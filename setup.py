from distutils.core import setup, Extension
import os

udt_dir = os.path.join(os.path.dirname(__file__),'..', 'udt', 'udt4', 'src')

module = Extension(
    '_udt',
    sources=['udt_py.cxx'],
    include_dirs=[".", udt_dir],
    libraries=['resolv', 'socket', 'rt', 'Cstd'] if os.uname()[0] == 'SunOS' else ['resolv'],
    extra_objects=[os.path.join(udt_dir, 'libudt.a')],
)

setup(
    name='udt_py',
    version='1.0',
    description='Python bindings for UDT',
    ext_modules=[module],
    py_modules=['udt']
)
