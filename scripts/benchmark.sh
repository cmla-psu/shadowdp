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
#!/bin/bash
passed=()
errored=()

# handles ctrl-c
trap ctrl_c INT

function ctrl_c() {
    exit 1
}

check()
{
    shadowdp check $1;
    if [[ $? == 0 ]]; then
        passed+=("$1")
    else
        errored+=("$1")
    fi
    echo ''
}

check "examples/original/noisymax.c"
check "examples/original/sparsevector.c"
# apply setting epsilon technique to solve non-linearity
check "examples/original/sparsevectorN.c -e NN"
check "examples/original/gapsparsevector.c -e NN"
check "examples/original/numsparsevector.c -e 1"
check "examples/original/numsparsevectorN.c -e NN"
check "examples/original/partialsum.c -e 1"
check "examples/original/prefixsum.c -e 1"
check "examples/original/smartsum.c -e 1 -g 2"

return_val=0
echo -e "Report: \e[32m ${#passed[@]} files passed. \e[0m\e[31m${#errored[@]} files failed.\e[0m"

if [[ ${#errored[@]} != 0 ]]; then
    return_val=1
    echo -e "\e[31mFailed commands:"
    for error in "${errored[@]}"
    do
        echo ${error}
    done
    echo -e "\e[0m"
fi

exit ${return_val}
