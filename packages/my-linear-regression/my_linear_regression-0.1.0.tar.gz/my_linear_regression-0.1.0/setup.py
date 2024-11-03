from setuptools import setup, find_packages

setup(
    name='my_linear_regression',
    version='0.1.0',
    author='Haitham',
    author_email='your_email@example.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/my_linear_regression/',
    license='LICENSE.txt',
    description='A simple linear regression model implemented from scratch.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[]  # Add any dependencies here if needed
)
