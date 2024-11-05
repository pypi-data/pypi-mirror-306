from setuptools import setup, find_packages 

setup(
    name = "MagpyCAS", 
    version = "1.0.6", 
    description = "A primitive package for creating mathematical structures from magmas to abelian groups, and determining their properties.", 
    author = "Skylar Korf", 
    author_email = "skorf60@gmail.com", 
    packages = find_packages(), 
    install_requires = ["iteration_utilities"], 
    license_file = "LICENSE", 
    long_description_type = "text/markdown",
    long_description = open("README.md").read()
)