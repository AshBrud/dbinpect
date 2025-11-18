from setuptools import setup, find_packages

setup(
    name="db-inspector",
    version="0.1",
    packages=find_packages(),
    py_modules=["scripts.db_inspector"],
    install_requires=[
        "SQLAlchemy>=2.0",
        "pydantic>=2.0",
        "python-dotenv>=1.0",
    ],
    entry_points={
        "console_scripts": [
            "analyze-db=scripts.db_inspector:main",
        ],
    },
)