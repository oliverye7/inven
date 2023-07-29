from setuptools import setup

setup(
    name="inven",
    version="0.1",
    description="Grocery tracking.",
    url="https://github.com/oliverye7/inven",
    author="Oliver Ye",
    author_email="oliverye7@berkeley.edu",
    packages=[],
    entry_points={
        "console_scripts": ["inven=client:cli"],
    },
    install_requires=["requests", "argparse", "toml", "pathlib"],
)
