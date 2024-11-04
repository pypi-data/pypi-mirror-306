from setuptools import setup, find_packages
setup(
    name="Mikel_Prueba",
    version="0.1.0",
    description="Prueba para aprender a subir librerías a Pypi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mikel Puerta",
    author_email="mikel.puerta@alumni.mondragon.edu",
    url="https://github.com/Mikel_Puerta/Mikel_Prueba",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3",    "License :: OSI Approved :: MIT License","Operating System :: OS Independent",],
    python_requires=">=3.6",
)
