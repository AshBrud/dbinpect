from setuptools import setup, find_packages
from pathlib import Path

# Lire le README pour la description longue
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="db-inspector",
    version="0.1.0",
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="Outil d'inspection et d'analyse de bases de données",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-user/dbinpect",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[
        "SQLAlchemy>=2.0",
        "pydantic>=2.0",
        "pydantic-settings>=2.0",
        "python-dotenv>=1.0",
    ],
    entry_points={
        "console_scripts": [
            "analyze-db=scripts.db_inspector:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
    ],
    keywords="database inspection sqlalchemy analysis",
)