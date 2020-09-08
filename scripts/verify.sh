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
#!/bin/sh

# handles ctrl-c
trap ctrl_c INT

function ctrl_c() {
    exit 1
}

shadowdp verify examples/transformed/noisymax.c
echo ''
shadowdp verify examples/transformed/sparsevector.c
echo ''
shadowdp verify examples/transformed/sparsevectorN.c
echo ''
shadowdp verify examples/transformed/sparsevectorN_rewrite.c -a '-setprop cpa.predicate.abstraction.initialPredicates=examples/transformed/sparsevectorN_predmap.txt'
echo ''
shadowdp verify examples/transformed/gapsparsevector.c
echo ''
shadowdp verify examples/transformed/gapsparsevector_rewrite.c -a '-setprop cpa.predicate.abstraction.initialPredicates=examples/transformed/gapsparsevector_predmap.txt'
echo ''
shadowdp verify examples/transformed/numsparsevector.c
echo ''
shadowdp verify examples/transformed/numsparsevectorN.c
echo ''
shadowdp verify examples/transformed/partialsum.c
echo ''
shadowdp verify examples/transformed/partialsum_rewrite.c
echo ''
shadowdp verify examples/transformed/prefixsum.c
echo ''
shadowdp verify examples/transformed/prefixsum_rewrite.c
echo ''
shadowdp verify examples/transformed/smartsum.c
echo ''
shadowdp verify examples/transformed/smartsum_rewrite.c
echo ''