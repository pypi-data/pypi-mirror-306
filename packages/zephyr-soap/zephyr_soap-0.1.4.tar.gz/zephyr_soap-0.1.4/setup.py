from setuptools import setup, find_packages
import pathlib

# Lire le fichier README avec encodage UTF-8
long_description = pathlib.Path("README.md").read_text(encoding="utf-8")

setup(
    name="zephyr_soap",
    version="0.1.4",
    author="gld",
    author_email="dimbugrace@gmail.com",
    description="Client SOAP pour utiliser les services SOAP d'Enedis",
    long_description=long_description,  # Utilise le contenu du README avec encodage UTF-8
    long_description_content_type="text/markdown",
    url="https://github.com/ZephyrIt0/Zephyr_soap_librairie",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests', 'zeep', 'pytz'
    ],
)
