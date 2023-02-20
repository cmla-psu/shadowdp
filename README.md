# ShadowDP

A verification tool for differentially private algorithms based on a new proving technique "Shadow Execution".

## Getting Started
### Overview
As described in Section 6 of our paper, ShadowDP consists of two components: (1) a type system that type checks the algorithm and generate transformed program (with explicit privacy cost variable calculations and other assertions). (2) a verifier to verify the assertions in the transformed program always hold. We implemeneted the first component as a trans-compiler from C to C in Python. For the second component we use an off-the-shelf model checking tool [CPA-Checker](https://cpachecker.sosy-lab.org/).

### Using Docker

Using docker is the easiest way to set everything up and running. Run

```bash
docker build -t shadowdp .
docker exec -it shadowdp /bin/bash
```

Then you'll be in a shell inside a docker container with ShadowDP ready to use.

## Usage
```bash
usage: __main__.py [-h] [-o OUT] [-c CHECKER] [-a ARGUMENTS] [-e EPSILON]
                   [-g GOAL]
                   OPTION FILE

positional arguments:
  OPTION                check - transform and verify. transform - only
                        transform the source code. verify - only verify the
                        transformed code.
  FILE

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     The output file name.
  -c CHECKER, --checker CHECKER
                        The checker path.
  -a ARGUMENTS, --arguments ARGUMENTS
                        The extra arguments for the checker.
  -e EPSILON, --epsilon EPSILON
                        Set epsilon to a specific value to solve the non-
                        linear issues.
  -g GOAL, --goal GOAL  The goal of the algorithm, default is epsilon-
                        differential privacy, specify this value to set
                        different goal. e.g., specify 2 to check for 2 *
                        epsilon-differential privacy
```

For example, you can use 

* `shadowdp transform examples/original/noisymax.c` to *only transform* `noisymax.c` to `noisymax_t.c` (by default we add `_t` suffix to the original filename, `-o` could be specified for different output name). 

* `shadowdp verify examples/transformed/noisymax.c` to *only verify* the transformed code.

* `shadowdp check examples/original/noisymax.c` to *transform and verify* `noisymax.c`.

We also provide a helper script at `scripts/benchmark.sh`, run `bash scripts/benchmark.sh` and it will run ShadowDP on all the case-studied algorithms in our paper.

To verify individual programs, for example in order to verify `noisymax.c`, run `shadowdp check noisymax.c`, and ShadowDP will type check and transform the source code, then invoke CPA-Checker to verify the transformed code. Argument `-c <dir> / --checker <dir>` can be used to specify the folder of pre-compiled CPA-Checker, by default it uses `./cpachecker` (You don't have to use it if followed the instructions).

All the case-studied algorithms are implemented in plain C in `examples/original` folder with names `noisymax.c` / `sparsevector.c` / `sparsevectorN.c` / `numsparsevector.c` / `numsparsevectorN.c` / `gapsparsevector.c` / `partiasum.c` / `prefixsum.c` / `smartsum.c`.

### Writing your own algorithm
Our tool has several assumptions of your source code:

* The first two lines of the function must be annotations, the first one being sensitivity definition and user-defined assumptions over variables, and second one being the types for the parameters.

* Use `Lap` as a function that draws laplace noise. It takes 2 parameters, first being the scale factor and second being the annotation for this random variable (as we discussed in the paper). 

* The first 3 function parameters must be `float epsilon`, `int size`, `float q[]` (order must be preserved but names can vary) which means the privacy budget, the size of input queries, and the query variable, respectively.

Otherwise it will raise exceptions.

See `examples/original/noisymax.c` as an example for the annotations.

### Non-linear rewrite
Due to the non-linear issues of CPA-Checker (discussed in Section 6.1 of our paper), CPA-Checker cannot directly verify the transformed code of `Gap Sparse Vector` / `Partial Sum` / `Prefix Sum` / `Smart Sum`. 

Thus we took 2 different approaches (rewrite assertions and setting epsilon to 1) to work around this issue, discussed in Section 6.1 and 6.2 in our paper. 

In our benchmark we used `epsilon = 1` approach to automatically verify the algorithms, we include all transformed code including the rewrite version (with suffix `_rewrite`) in `examples/transformed` folder for references. Run `bash scripts/verify.sh` to verify them all.

## Install Manually

If Docker isn't an available option for you, you can install ShadowDP manually following the steps below.

**System Requirements**.
Python 3.5 / 3.6 / 3.7 on Linux is required, Ubuntu 18.04 LTS is tested and recommended, though Ubuntu 16.04 LTS and other Linux distributions should also work. This is due to the requirements from the verification tool we use (i.e., [CPA-Checker](https://cpachecker.sosy-lab.org/)), which lacks many pre-compiled solver backends on other operating systems (e.g. MathSAT5 and z3 on macOS). 

In addition, `wget` package and JAVA 8 / 11 are required. Install them via
```bash
sudo apt-get update -y
sudo apt-get install python3 wget openjdk-11-jre
# `openjdk-11-jre` is not available under Ubuntu 16.04, you can either install JAVA 8 by
sudo apt-get install python3 wget openjdk-8-jre
# or add apt repository
add-apt-repository ppa:openjdk-r/ppa
apt-get install -y openjdk-11-jre
```

**Download CPA-Checker.** 
As pre-compiled CPA-Checker binaries are relatively large, we don't include them as part of this project, you'll have to download them yourself. Run `scripts/get_cpachecker.sh` to take care of the download for you.

**Install ShadowDP.**
`venv` is highly recommended in order not to interfere with your system packages (or if you prefer `virtualenv` / `Anaconda`, the setup is similar).

```bash
python -m venv venv
source venv/bin/acitvate
# now we're in virtual environment
pip install .
```

## Citing this work
Please consider citing the following [paper](https://arxiv.org/pdf/1903.12254.pdf) if you use this tool for academic research.
```tex
@inproceedings{wang2019shadowexecution,
 author = {Wang, Yuxin and Ding, Zeyu and Wang, Guanhong and Kifer, Daniel and Zhang, Danfeng},
 title = {Proving Differential Privacy with Shadow Execution},
 booktitle = {Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design and Implementation},
 series = {PLDI 2019},
 year = {2019},
 isbn = {978-1-4503-6712-7},
 location = {Phoenix, AZ, USA},
 pages = {655--669},
 numpages = {15},
 url = {http://doi.acm.org/10.1145/3314221.3314619},
 doi = {10.1145/3314221.3314619},
 acmid = {3314619},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Differential privacy, dependent types},
} 
```

## License
[MIT](https://github.com/yxwangcs/shadowdp/blob/master/LICENSE).
