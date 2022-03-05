from setuptools import find_packages,setup

setup(
    name="findata",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "yfinance",
        "matplotlib",
        "openpyxl"
    ],
    entry_points={
        "console_scripts": [
            "findata=findata:cli"
        ],
    },
)
