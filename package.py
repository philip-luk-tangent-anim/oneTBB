# -*- coding: utf-8 -*-

name = 'tbb'

version = '2017.U6'

authors = [
    'philip.luk'
]

requires = [
]

build_requires = [
    'python-2',
    'ninja',
]

variants = [
    ['platform-windows', 'arch-x86_64'],
    ['platform-linux', 'arch-x86_64'],
]

build_command = "python {root}/install_tbb.py"

def commands():
    pass

