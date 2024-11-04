from setuptools import setup,find_packages

setup(
    name='libreria_otaku',
    version="0.1.0",
    description="Descripción breve de tu librería",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ola",
    author_email="mikelarturo.balleste@alumni.mondragon.edu",
    url="https://github.com/mikelb/libreria_otaku",
    packages=find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)