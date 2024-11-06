from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="them4tch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Franco Romeo",
    description="Una biblioteca para consultar los curso de Hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
