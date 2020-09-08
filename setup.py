from setuptools import setup, find_packages

# Get the long description from the relevant file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='shadowdp',
    version='0.1',
    description='Verification Tool for Differential Privacy. '
                'Code for [PLDI\'19] "Proving Differential Privacy with Shadow Execution".',
    long_description=long_description,
    url='https://github.com/cmla-psu/shadowdp',
    author='Yuin Wang/Zeyu Ding/Guanhong Wang/Daniel Kifer/Danfeng Zhang',
    author_email='{yxwang,zyding,gpw5092}@psu.edu, {dkifer,zhang}@cse.psu.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Programming Language :: Differential Privacy',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='Programming Language, Differential Privacy',
    packages=find_packages(exclude=['tests']),
    install_requires=['pycparser', 'coloredlogs', 'sympy', 'z3-solver'],
    extras_require={
        'test': ['pytest-cov', 'pytest', 'coverage'],
    },
    entry_points={
        'console_scripts': [
            'shadowdp=shadowdp.__main__:main',
        ],
    },
)
