import setuptools

setuptools.setup(
    name="ImageDB",
    version="0.0.1",
    author="Foresight",
    author_email="sv.sv82@outlook.com",
    packages=["ImageDB"],
    description="A package for managing image with PostgresSQL",
    url="https://github.com/JumpingSquid/ImageDB",
    license='GPT',
    python_requires='>=3.6',
    install_requires=[
        "psycopg2"
    ]
)