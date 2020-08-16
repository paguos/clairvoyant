# flake8: noqa
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    install_requires=[
        "certifi==2020.6.20",
        "cmdstanpy==0.4",
        "convertdate==2.2.1",
        "cycler==0.10.0",
        "cython==0.29.21; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "ephem==3.7.7.1",
        "fbprophet==0.6",
        "holidays==0.10.3",
        "joblib==0.16.0; python_version >= '3.6'",
        "kiwisolver==1.2.0; python_version >= '3.6'",
        "korean-lunar-calendar==0.2.1",
        "loguru==0.5.1",
        "lunarcalendar==0.0.9; python_version >= '2.7' and python_version < '4'",
        "matplotlib==3.3.1",
        "numpy==1.19.1; python_version >= '3.6'",
        "pandas==1.1.0",
        "pillow==7.2.0; python_version >= '3.5'",
        "pymeeus==0.3.7",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pystan==2.19.1.1",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2020.1",
        "scikit-learn==0.23.2; python_version >= '3.6'",
        "scipy==1.5.2; python_version >= '3.6'",
        "setuptools-git==1.2",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "sklearn==0.0",
        "threadpoolctl==2.1.0; python_version >= '3.5'",
    ],
    name="clairvoyant",
    version="0.0.1",
    author="Pablo Osinaga",
    author_email="paguos@gmail.com",
    description="A toolkit for predicting the future",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paguos/clairvoyant",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
