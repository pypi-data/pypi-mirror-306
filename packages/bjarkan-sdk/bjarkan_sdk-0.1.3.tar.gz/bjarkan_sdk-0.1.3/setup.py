from setuptools import setup

if __name__ == "__main__":
    setup(
        name="bjarkan-sdk",
        package_dir={"": "src"},
        packages=["bjarkan"],
        install_requires=[
            "ccxt>=4.1.13",
            "pydantic>=2.5.2",
            "loguru>=0.7.2",
            "python-dotenv>=1.0.0",
        ],
    )
