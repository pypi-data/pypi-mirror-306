import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "sliderplot",
    version = "0.1.0",
    author = "Nathan Gripon",
    author_email = "n.gripon@gmail.com",
    description = "Turn a function into an interactive plot with a single line of code",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ngripon/sliderplot",
    project_urls = {
        "Bug Tracker": "https://github.com/ngripon/sliderplot/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.10",
    install_requires=['numpy','panel','bokeh', 'jupyter_bokeh']
)