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
set e
#wget https://vcloud.sosy-lab.org/cpachecker/webclient/tool/ -O cpachecker.zip
#mkdir cpachecker
#unzip cpachecker.zip -d cpachecker
# compile cpachecker on our own
git clone https://github.com/sosy-lab/cpachecker.git cpachecker-build
cd cpachecker-build 
# switch to revision 30894 since it strenthens the type conversion from int to float
# which is required by shadowdp
# see https://groups.google.com/d/msg/cpachecker-users/LK4DzRhR7Xc/T-VgOIf3BgAJ
git reset --hard 57e456aad032bcb2e42911202976423b785797cb
ant dist-unix-zip -Dnamez=cpachecker
unzip ./cpachecker.zip -d ../
cd ..
chmod +x cpachecker/scripts/cpa.sh
rm -rf cpachecker-build