from setuptools import setup, find_packages

setup(
    name="PassGenerated",  # Nombre único de tu librería en PyPI
    version="0.1.2",  # Usa el formato mayor.menor.parche
    author="JhimmyGC",
    author_email="pbbanger32@gmail.com",
    description="Lib for generating passwords",  # Descripción de tu librería
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Liounex/pyLibR.git",  # URL del repositorio
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],  # Lista de dependencias, si tienes alguna
)
