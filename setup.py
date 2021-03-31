import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="config_wrapper",
    version="0.0.11",
    author="Piotr Zielski",
    author_email="zielskipiotr@gmail.com",
    description="Simple wrapper for cofigparser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pzielski/config-wrapper",
    project_urls={
        "Bug Tracker": "https://github.com/pzielski/config-wrapper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)