from setuptools import setup, find_packages

setup(
    name="RedPanPy",                # Required: package name
    version="0.0.5",                    # Required: package version
    author="Rafa Rayes",
    author_email="rafa@rayes.com",
    description="Framework for developing apps with Python and HTML",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,          # Include non-Python files as package data
    package_data={
        "RedPanPy": ["qwebchannel.js"],  # List of files to include
    },
    url="https://github.com/rafa-rrayes/RedPanPy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyQt5",
        "PyQtWebEngine",
    ],
)
