import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypalazzetti",
    version="0.1.8",
    author="Vincent Roukine",
    author_email="vincent.roukine@gmail.com",
    description="A Python library to access and control a Palazzetti stove through a Palazzetti Connection Box",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/dotvav/python-palazzetti-api",
    packages=setuptools.find_packages(),
    install_requires=["aiohttp>=3.10.3"],
    python_requires=">=3.6",
    include_package_data=True,
)
