from setuptools import setup, find_packages

setup(
    name='marfyl_metadata_service',
    version='0.3.0',
    description='A service to process metadata from headers',
    author='Eduardo Ponce',
    author_email='poncejones@gmail.com',
    packages=find_packages(),
    install_requires=[
        # Here you can add necessary dependencies
    ],
    python_requires='>=3.9',
)