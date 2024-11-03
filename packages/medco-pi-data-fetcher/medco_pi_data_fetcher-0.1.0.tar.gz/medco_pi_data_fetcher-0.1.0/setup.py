from setuptools import setup, find_packages

setup(
    name="medco_pi_data_fetcher",
    version="0.1.0",
    description="A package to fetch data from PI System using PI Web API",
    author="Wiguna Kurniawan",
    author_email="wiguna_kurniawan@ymai.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas"
    ],
    python_requires='>=3.6',
)
