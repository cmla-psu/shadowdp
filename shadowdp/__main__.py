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
import argparse
import coloredlogs
import os.path
import sys
import time
import logging
from pycparser import parse_file
from pycparser.c_generator import CGenerator
from shadowdp.core import ShadowDPTransformer
from shadowdp.exceptions import *
from shadowdp.checker import check


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', fmt='%(levelname)s:%(module)s: %(message)s')

__HEADER = r"""extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_float(void);
extern int __VERIFIER_nondet_int();
extern void __VERIFIER_assume(int);
extern void __assert_fail();
#define __VERIFIER_assert(cond) { if(!(cond)) { __assert_fail(); } }
#define Abs(x) ((x) < 0 ? -(x) : (x))
typedef enum { false = 0, true = 1 } bool;
    
"""

__FUNCTION_MAP = {
    'assert': '__VERIFIER_assert',
    'assume': '__VERIFIER_assume',
    'havoc': '__VERIFIER_nondet_float'
}


def main(argv=sys.argv[1:]):
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument('option', metavar='OPTION', type=str, nargs=1,
                            help='check - transform and verify.\n'
                                 'transform - only transform the source code.\n'
                                 'verify - only verify the transformed code.')
    arg_parser.add_argument('file', metavar='FILE', type=str, nargs=1)
    arg_parser.add_argument('-o', '--out',
                            action='store', dest='out', type=str,
                            help='The output file name.', required=False)
    arg_parser.add_argument('-c', '--checker',
                            action='store', dest='checker', type=str, default='./cpachecker',
                            help='The checker path.', required=False)
    arg_parser.add_argument('-a', '--arguments',
                            action='store', dest='arguments', type=str, default=None,
                            help='The extra arguments for the checker.', required=False)
    arg_parser.add_argument('-e', '--epsilon',
                            action='store', dest='epsilon', default=None,
                            help='Set epsilon to a specific value to solve the non-linear issues.', required=False)
    arg_parser.add_argument('-g', '--goal',
                            action='store', dest='goal', type=str, default=None,
                            help='The goal of the algorithm, default is epsilon-differential privacy, specify'
                                 'this value to set different goal. '
                                 'e.g., specify 2 to check for 2 * epsilon-differential privacy', required=False)
    results = arg_parser.parse_args(argv)
    results.file = results.file[0]
    results.out = results.file[0:results.file.rfind('.')] + '_t.c' if results.out is None else results.out

    if results.option[0] not in ('check', 'transform', 'verify'):
        logger.error('Option should be check / transform / verify')
        return 1

    if not os.path.exists(results.file):
        logger.error('File {} doesn\'t exists'.format(results.file))
        return 1

    if results.option[0] != 'transform':
        if not os.path.isdir(results.checker):
            logger.error('Path for cpachecker must be the root directory, got {}'.format(results.checker))
            logger.error('Please run scripts/get_cpachecker.sh to get a precompiled version of cpachecker')
            return 1
        script_folder = os.path.join(results.checker, 'scripts')
        if not (os.path.exists(script_folder) and os.path.exists(os.path.join(script_folder, 'cpa.sh'))):
            logger.error('{} doesn\'t exist, cpachecker might be broken'.format(os.path.join(script_folder, 'cpa.sh')))
            logger.error('Please run scripts/get_cpachecker.sh to get a precompiled version of cpachecker')
            return 1

    if results.option[0] == 'check' or results.option[0] == 'transform':
        # parse the source code
        logger.info('Parsing {}'.format(results.file))
        start = time.time()
        ast = parse_file(results.file, use_cpp=True, cpp_path='gcc', cpp_args=['-E'])
        transformer = ShadowDPTransformer(function_map=__FUNCTION_MAP,
                                          set_epsilon=results.epsilon, set_goal=results.goal)

        try:
            transformer.visit(ast)
        except NoParameterAnnotationError as e:
            logger.error('{} First statements must be a string containing annotation'.format(str(e.coord)))
            return 1
        except NoSamplingAnnotationError as e:
            logger.error('{} Sampling command lack annotation'.format(str(e.coord)))
            return 1
        except ReturnDistanceNotZero as e:
            logger.error('{}: Aligned distance of return variable {} is not zero ({})'
                         .format(str(e.coord), e.name, e.distance))
            return 1
        except SamplingCommandMisplaceError as e:
            logger.error('{}: Cannot use sampling command in diverging branch.'.format(e.coord))
            return 1
        except SamplingCommandInjectivityError as e:
            logger.error('{}: Distance annotation {} for {} isn\'t injective'.format(e.coord, e.eta, e.annotation))
        else:
            # write the transformed code
            with open(results.out, 'w') as f:
                # write verifier headers
                f.write(__HEADER)
                f.write(CGenerator().visit(ast))

            logger.info('Transformation finished in {0:.3f} seconds'.format(time.time() - start))

    is_verified = False
    if results.option[0] == 'check':
        is_verified = check(results.checker, results.out, results.arguments)
    elif results.option[0] == 'verify':
        is_verified = check(results.checker, results.file, results.arguments)

    # shell code 0 means SUCCESS
    return 0 if is_verified else 1


if __name__ == '__main__':
    main()
