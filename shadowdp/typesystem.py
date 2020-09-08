# MIT License
#
# Copyright (c) 2018-2019 Yuxin (Ryan) Wang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import copy
from collections import OrderedDict
from pycparser.c_parser import CParser
from pycparser.c_generator import CGenerator
from pycparser.c_ast import NodeVisitor
from pycparser import c_ast


_parser = CParser()
_generator = CGenerator()


def convert_to_ast(expression):
    # this is a trick since pycparser cannot parse expression directly
    ast = _parser.parse('int placeholder(){{{};}}'.format(expression)).ext[0].body.block_items[0]
    return ast


def is_node_equal(node_1, node_2):
    """ check if two expression AST nodes are equal since pycparser doesn't provide such property
    :param node_1: First expression node
    :param node_2: Second expression node
    :return: Boolean
    """
    # naive comparison, can be optimized
    return node_1.__repr__() == node_2.__repr__()


class _DistanceSimplifier(NodeVisitor):
    """Simplifies a given distance c_ast node using conditions.
    e.g. distance x + y > 0 ? 2 : 0 would be simplified to 2 if condition (x + y > 0) is given."""
    def __init__(self, condition, is_true):
        self._condition = condition
        self._is_true = is_true

    def _simplify(self, ternary_node):
        assert isinstance(ternary_node, c_ast.TernaryOp)
        if is_node_equal(ternary_node.cond, self._condition):
            return ternary_node.iftrue if self._is_true else ternary_node.iffalse
        return ternary_node

    def visit_BinaryOp(self, node):
        node.left = self._simplify(node.left) if isinstance(node.left, c_ast.TernaryOp) else node.left
        node.right = self._simplify(node.right) if isinstance(node.right, c_ast.TernaryOp) else node.right
        for c in node:
            self.visit(c)

    def visit_UnaryOp(self, node):
        node.expr = self._simplify(node.expr) if isinstance(node.expr, c_ast.TernaryOp) else node.expr
        self.visit(node.expr)

    def simplify(self, node):
        # copy a node in order not to mess with parameter
        node = copy.copy(node)
        if isinstance(node, c_ast.TernaryOp):
            node = self._simplify(node)
        self.visit(node)
        return node


class TypeSystem:
    """ TypeSystem keeps track of the distances of each variable. The distance of each variable is internally
    represented by c_ast node, and gets simplified and casted to strings when get_distance method is called"""
    _EXPR_NODES = (c_ast.BinaryOp, c_ast.TernaryOp, c_ast.UnaryOp, c_ast.ID, c_ast.Constant, c_ast.ArrayRef)

    def __init__(self, types=None):
        if types:
            self._types = types
        else:
            self._types = OrderedDict()

    def __str__(self):
        # convert AST representation to code representation for better human-readability
        return '{{{}}}'.format(
            ', '.join('{}: [{}, {}]'.format(name,
                                            aligned if aligned == '*' else _generator.visit(aligned),
                                            shadow if shadow == '*' else _generator.visit(shadow))
                      for name, (aligned, shadow) in self._types.items()
                      )
        )

    def __len__(self):
        return len(self._types)

    def __repr__(self):
        return self._types.__repr__()

    def __eq__(self, other):
        if isinstance(other, TypeSystem):
            return self._types.__repr__() == other.__repr__()
        else:
            return False

    def __contains__(self, item):
        return self._types.__contains__(item)

    def copy(self):
        return TypeSystem(copy.deepcopy(self._types))

    def clear(self):
        self._types.clear()

    def variables(self):
        for name in self._types.keys():
            yield name, self.get_distance(name)

    def apply(self, condition, is_true):
        simplifier = _DistanceSimplifier(condition, is_true)
        for name in self._types.keys():
            self._types[name] = \
                [simplifier.simplify(distance) if distance != '*' else distance for distance in self._types[name]]

    def diff(self, other):
        assert isinstance(other, TypeSystem)
        for name, *_ in other.variables():
            if name not in self._types:
                yield (name, True)
                yield (name, False)
            else:
                aligned, shadow = self._types[name]
                other_aligned, other_shadow = other.get_raw_distance(name)
                if not is_node_equal(aligned, other_aligned):
                    yield (name, True)
                if not is_node_equal(shadow, other_shadow):
                    yield (name, False)

    def merge(self, other):
        assert isinstance(other, TypeSystem)
        for name, *_ in other.variables():
            if name not in self._types:
                self._types[name] = other.get_raw_distance(name)
            else:
                cur_align, cur_shadow = self._types[name]
                other_align, other_shadow = other.get_raw_distance(name)
                if not (cur_align == other_align == '*' or is_node_equal(cur_align, other_align)):
                    self._types[name][0] = '*'
                if not (cur_shadow == other_shadow == '*' or is_node_equal(cur_shadow, other_shadow)):
                    self._types[name][1] = '*'

    def get_raw_distance(self, name):
        """ return the raw distance, in AST node representation.
        :param name: The name of the variable.
        :return: (Aligned raw distance, Shadow raw distance), both of ast node type.
        """
        return self._types[name]

    def get_distance(self, name):
        """ get the distance(align, shadow) of a variable, in str representation.
        :param name: The name of the variable.
        :return: (Aligned distance, Shadow distance) of the variable.
        """
        return tuple('*' if distance == '*' else _generator.visit(distance) for distance in self._types[name])

    def update_distance(self, name, align, shadow):
        # try simplify
        from sympy import simplify

        align = str(align).replace('[', '__LEFTBRACE__').replace(']', '__RIGHTBRACE__')
        shadow = str(shadow).replace('[', '__LEFTBRACE__').replace(']', '__RIGHTBRACE__')
        try:
            align = simplify(align)
        except Exception:
            pass
        try:
            shadow = simplify(shadow)
        except Exception:
            pass
        align = str(align).replace('__LEFTBRACE__', '[').replace('__RIGHTBRACE__', ']')
        shadow = str(shadow).replace('__LEFTBRACE__', '[').replace('__RIGHTBRACE__', ']')
        # convert to internal AST representation
        align = convert_to_ast(align) if align != '*' else '*'
        shadow = convert_to_ast(shadow) if shadow != '*' else '*'
        if name not in self._types:
            self._types[name] = [align, shadow]
        else:
            cur_aligned, cur_shadow = self._types[name]
            if not is_node_equal(cur_aligned, align):
                self._types[name][0] = align
            if not is_node_equal(cur_shadow, shadow):
                self._types[name][1] = shadow
