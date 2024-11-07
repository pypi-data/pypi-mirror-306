project(
    'kvh',
    'cpp',
    version: run_command('cat', 'kvh/version.txt', check: true).stdout().strip(),
    default_options: [
        'cpp_std=c++11',
    ],
)

py = import('python').find_installation(pure: false)
pybind11_dep = dependency('pybind11')

py.extension_module('ckvh',
    'kvh/ckvh.cpp',
    install: true,
    dependencies : [pybind11_dep],
    subdir: 'kvh'
)

py.install_sources(
    ['kvh/__init__.py', 'kvh/kvh.py', 'kvh/version.txt', './salut.kvh'],
    pure: false,
    subdir: 'kvh',
)
