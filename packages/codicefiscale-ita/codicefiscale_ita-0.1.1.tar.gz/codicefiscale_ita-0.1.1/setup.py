from setuptools import setup, find_packages

setup(
    name="codicefiscale-ita",
    version="0.1.1",
    description="Libreria per generare e validare codici fiscali italiani",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Filippo Casadei",
    author_email="filippo.casadei2004@gmail.com",
    url="https://github.com/FilippoCasadei/py-codicefiscale-lib.git",
    packages=find_packages(exclude=["tests*"]) + ["codicefiscale.data"],
    include_package_data=True,
    package_data={"codicefiscale": ["data/*.csv"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
