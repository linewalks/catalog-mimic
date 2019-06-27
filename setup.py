import io

from setuptools import find_packages, setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="catalog-mimic",
    version="0.1",
    url="https://github.com/linewalks/catalog-mimic",
    license="GNU AFFERO GENERAL PUBLIC LICENSE",
    maintainer="Linewalks Tech Group",
    maintainer_email="web@linewalks.com",
    description="MIMIC-III Data Catalog",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "PyMySQL",
        "SQLAlchemy",
        "numpy",
        "pandas",
        "flake8",
        "flake8-quotes",
        "psycopg2-binary"
    ],
    extras_require={
        "test": [
            "pytest",
            "coverage",
        ],
    },
)
