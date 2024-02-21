from setuptools import setup, find_packages

with open('requirements.txt', 'r') as file:
    install_reqs = file.read().split("\n")
    file.close()

setup(
    name='Graph_Processing',
    install_requires=install_reqs,
    packages=find_packages(),
    )

# setup(name='Graph_Processing', version='1.0', packages=find_packages())
