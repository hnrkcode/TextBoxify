import setuptools


def read(filename):
    """Return file content."""
    with open(filename, "r") as f:
        return f.read()


setuptools.setup(
    name="textboxify",
    version="0.2.0",
    author="Henrik Petersson",
    author_email="henrik@tutamail.com",
    url="https://github.com/hnrkcode/TextBoxify",
    description="Pygame package to easily create dialog boxes for games.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=["pygame"],
    packages=setuptools.find_packages(),
    package_data={
        "textboxify": [
            "data/border/*/*.png",
            "data/indicator/*.png",
            "data/portrait/*.png",
        ],
    },
)
