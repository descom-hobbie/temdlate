#/bin/bash
pip3 install cython &&
cython main.py --embed &&
PYTHONLIBVER=python$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$(python3-config --abiflags) &&
gcc -Os $(python3-config --includes) main.c -o temdlate $(python3-config --ldflags) -l$PYTHONLIBVER &&
rm -rf main.c