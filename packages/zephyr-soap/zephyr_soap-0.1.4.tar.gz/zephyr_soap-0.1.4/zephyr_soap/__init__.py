# zephyr_soap/__init__.py

# Importez la classe principale du client SOAP à partir de core.py
from .core import SoapClient  # Importation depuis le fichier core.py

__all__ = ['SoapClient']  # Rend la classe SoapClient disponible lors de l'importation
