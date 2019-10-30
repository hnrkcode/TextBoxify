import setuptools

setuptools.setup(
    name="textboxify",
    version="0.1.0",
    author="Henrik Petersson",
    author_email="henrik@tutamail.com",
    url="https://github.com/hnrkcode/TextBoxify",
    description="Pygame package to easily create dialog boxes for games.",
    packages=setuptools.find_packages(),
    package_data={
        "textboxify": [
            "data/border/default/*.png",
            "data/indicator/*.png",
            "data/portrait/*.png",
        ],
    },
)
