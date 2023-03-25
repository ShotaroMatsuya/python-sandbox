try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    name='python_programming_demo_app',
    version='0.0.2',
    packages=find_packages(),
    # You could use find_packages if setuptools is installed. 
    package_data={'roboter': ['templates/*.txt']},
    url='',
    license='MIT',
    author='jsakai',
    author_email='example@example.com',
    # You can specify install_requires if setuptools is installed
    install_requires=['termcolor==1.1.0'],
    long_description=open('README.txt').read(),
    tests_require=['pytest'],
    setup_requires=["pytest-runner"]
    # test_suits='tests'
)
