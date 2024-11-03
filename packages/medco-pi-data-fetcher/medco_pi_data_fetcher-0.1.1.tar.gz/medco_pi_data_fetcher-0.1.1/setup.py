from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="medco-pi-data-fetcher",
    version="0.1.1",  # Pastikan untuk memperbarui versi setiap kali ada perubahan
    author="Wiguna Kurniawan",
    author_email="youremail@example.com",
    description="A package to fetch data from PI System using PI Web API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WigunaKurniawan/medco-pi-data-fetcher",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "pandas",
        # Tambahkan dependencies lain jika diperlukan
    ],
)
