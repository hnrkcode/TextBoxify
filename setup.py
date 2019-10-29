import setuptools

setuptools.setup(
    name="TextBoxify",
    description="Text box engine for games written in Pygame.",
    packages=setuptools.find_packages(),
    package_data={
        "textboxify": [
            "data/border/default/*.png",
            "data/indicator/*.png",
            "data/portrait/*.png",
        ]
    },
)
