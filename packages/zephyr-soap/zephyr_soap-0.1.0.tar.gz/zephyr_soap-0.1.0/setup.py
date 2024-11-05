from setuptools import setup, find_packages

setup(
    name="zephyr_soap",                     # Nom du package PyPI
    version="0.1.0",                       
    author="gld",                         
    author_email="dimbugrace@gmail.com",    #  adresse email
    description="Client SOAP pour utiliser les services SOAP d'Enedis",    
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZephyrIt0/Zephyr_soap_librairie",  #dépôt du projet
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests', 'zeep','pytz'
    ],
)
