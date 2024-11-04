# setup.py
import setuptools

setuptools.setup(
    name = "leonardo_floresgonzalez_calculator_5436",
    version = "0.3.0",
    author="Leonardo Flores Gonzalez",
    author_email = "leof7812@gmail.com",
    description="An advanced calculator package",
    long_description="I am building this calculator package for CS-122 class",
    long_description_content_type="text/markdown",
    url="https://github.com/leo7812/my_calculator",
    license="MIT",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    include_package_data=True
)