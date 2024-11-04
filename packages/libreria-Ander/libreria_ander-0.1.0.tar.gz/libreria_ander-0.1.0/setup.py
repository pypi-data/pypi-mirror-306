from setuptools import setup, find_packages
setup(
    name="libreria_Ander",
    version="0.1.0",
    description="La librería de Ander Oficial",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ander",
    author_email="tuemail@example.com",
    url="https://github.com/andercrispy/lib",
    packages=find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent",
    ],
    python_requires=">=3.6", )