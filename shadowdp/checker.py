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
from collections import OrderedDict
from queue import Queue
import os
import subprocess
import threading
import logging
import shutil
import re
logger = logging.getLogger(__name__)


def _thread_wait_for(results, name, process):
    try:
        # wait for 30 seconds
        out, err = process.communicate(timeout=30)
        if r'Verification result: TRUE' in str(out):
            results.put((True, name, None, None))
        else:
            results.put((False, name, out, err))
    except subprocess.TimeoutExpired:
        results.put((False, '30 seconds Timeout', '', ''))


def check(checkerpath, path, args=None):
    funcname = os.path.splitext(os.path.basename(path))[0]
    args = args.split(' ') if args else ''

    logger.info('Start checking {} with multiple solvers(MathSat, Z3, SMT-Interpol)...'.format(path))
    processes = OrderedDict()
    processes['MathSat'] = subprocess.Popen(
        [checkerpath + '/scripts/cpa.sh', '-predicateAnalysis', path, '-preprocess',
         '-setprop', 'cpa.predicate.encodeFloatAs=RATIONAL', '-setprop', 'cpa.predicate.encodeBitvectorAs=INTEGER',
         '-setprop', 'solver.nonLinearArithmetic=USE', '-setprop', 'output.path=output-{}-MathSat'.format(funcname),
         '-setprop', 'solver.solver=MATHSAT5',
         *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes['Z3'] = subprocess.Popen(
        [checkerpath + '/scripts/cpa.sh', '-predicateAnalysis', path, '-preprocess',
         '-setprop', 'cpa.predicate.encodeFloatAs=RATIONAL', '-setprop', 'cpa.predicate.encodeBitvectorAs=INTEGER',
         '-setprop', 'solver.nonLinearArithmetic=USE', '-setprop', 'output.path=output-{}-Z3'.format(funcname),
         '-setprop', 'solver.solver=Z3',
         *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes['SMTInterpol'] = subprocess.Popen(
        [checkerpath + '/scripts/cpa.sh', '-predicateAnalysis-linear', path, '-preprocess',
         '-setprop', 'solver.solver=smtinterpol', '-setprop', 'output.path=output-{}-SMTInterpol'.format(funcname)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # start threads to wait for results
    results = Queue()
    threads = set()
    for name, proc in processes.items():
        thread = threading.Thread(target=_thread_wait_for, args=(results, name, proc))
        threads.add(thread)
        thread.start()

    # get the results
    errors = set()
    is_verified = False
    verified_solver = ''
    for _ in range(len(processes)):
        verified, name, out, err = results.get()
        if verified:
            logger.info('{} verified with {}.'.format(path, name))
            # open and read report to find
            with open('./output-{}-{}/Statistics.txt'.format(funcname, name)) as report:
                all_report = report.read()
                time = re.search(r'Total time for CPAchecker[:\s<>/a-zA-Z]*([0-9]+\.[0-9]+s)', all_report).groups()
                logger.info('Verification finished in {}'.format(time[0]))
            logger.info('CPA-Checker reports can be found at ./output-{}-{}'.format(funcname, name))
            verified_solver = name
            is_verified = True
            break
        else:
            # log the error if this solver fails
            errors.add((name, out, err))

    # clean up threads and processes
    for proc in processes.values():
        proc.kill()
        proc.wait()
    for thread in threads:
        thread.join()

    # remove failed solver output
    for solver in ('MathSat', 'Z3', 'SMTInterpol'):
        if solver != verified_solver:
            shutil.rmtree('./output-{}-{}'.format(funcname, solver))

    # if no solvers can verify the program
    if not is_verified:
        logger.warning('No solvers can verify the program, error messages shown below:')
        for name, out, err in errors:
            logger.warning('{}:\n\tout: {}\n\terr:{}'.format(name, out.decode('ascii'), err.decode('ascii')))

    return is_verified
