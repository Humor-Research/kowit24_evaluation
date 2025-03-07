from setuptools import setup, find_packages

setup(
    name="kowit24_evaluation",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pymorphy3",
        "pandas"
    ],
    author="Alexander Baranov",
    author_email="alexanderbaranof@gmail.com",
    description="Evaluation tools for KoWit-24 interpretation tasks",
    url="https://github.com/Humor-Research/kowit24_evaluation",
)