from setuptools import setup, find_packages

setup(
    name="refreshrate",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        'wmi'
    ],
    author="Ayaan",
    author_email="iamayaanalee@gmail.com",
    description="A python package that fetchs your monitor refresh rate.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruskydev/refreshrate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
