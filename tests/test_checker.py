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
from shadowdp.checker import check


def test_check():
    assert check('./cpachecker', './examples/transformed/noisymax.c')
    assert check('./cpachecker', './examples/transformed/sparsevector.c')
    assert check('./cpachecker', './examples/transformed/sparsevectorN.c')
    assert check('./cpachecker', './examples/transformed/numsparsevector.c')
    assert check('./cpachecker', './examples/transformed/numsparsevectorN.c')
    assert check('./cpachecker', './examples/transformed/gapsparsevector.c')
    assert check('./cpachecker', './examples/transformed/partialsum.c')
    assert check('./cpachecker', './examples/transformed/partialsum_rewrite.c')
    assert check('./cpachecker', './examples/transformed/prefixsum.c')
    assert check('./cpachecker', './examples/transformed/prefixsum_rewrite.c')
    assert check('./cpachecker', './examples/transformed/smartsum.c')
    assert check('./cpachecker', './examples/transformed/smartsum_rewrite.c')
    assert check('./cpachecker', './examples/transformed/sparsevectorN_rewrite.c',
                 '-setprop cpa.predicate.abstraction.initialPredicates='
                 './examples/transformed/sparsevectorN_predmap.txt')
    assert check('./cpachecker', './examples/transformed/gapsparsevector_rewrite.c',
                 '-setprop cpa.predicate.abstraction.initialPredicates='
                 './examples/transformed/gapsparsevector_predmap.txt')

