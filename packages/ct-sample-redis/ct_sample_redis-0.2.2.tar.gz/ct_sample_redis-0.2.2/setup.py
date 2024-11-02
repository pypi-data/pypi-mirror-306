from setuptools import find_packages, setup

setup(
    name='ct_sample_redis',
    packages=find_packages(),
    version='0.2.2',  # Increment version
    description='Common custom library for Redis',
    author='credenti',
    install_requires=["redis==5.0.3", "Flask>=2.0.2"],  # Include the required libraries
)
