from setuptools import setup, find_packages

setup(
    name='precise_rounding',
    version='0.1.2',
    packages=[''],
    package_dir={'': 'precise_rounding'},
    url='https://github.com/slawomirmarczynski/precise_rounding',
    license='BSD-3-Clause',
    author='Sławomir Marczyński',
    author_email='',
    description='Rounds a measurement value and its uncertainty '
                'to a specified number of significant digits.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
