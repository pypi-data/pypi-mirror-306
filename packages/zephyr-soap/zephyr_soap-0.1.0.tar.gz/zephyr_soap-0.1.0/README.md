# Zephyr SOAP Client

**Auteur** : Grâce LUSAKUMUNU DIMBU

## Description

Zephyr SOAP Client est une bibliothèque Python conçue pour interagir avec un service SOAP en utilisant des certificats et des informations de connexion. Ce client permet l’accès à divers services, notamment la consultation de données contractuelles, la collecte de mesures, et bien plus.

## Installation

Pour installer ce package, publiez-le sur PyPI et installez-le avec pip :

```bash
pip install zephyr_soap

```

# Configuration
Placez un fichier de configuration settings.json dans le dossier SGE/Conf/. Ce fichier doit contenir les chemins de journalisation et les URL des services SOAP.

Exemple de configuration (settings.json)
```json
{
    "certificats": {
        "client_cert": "",
        "client_key": "",
        "sge_homologation": "",
        "ca_cert": ""
    },
    "connexion": {
        "nni": "",
        "password": "",
        "login": "",
        "contratId": ""
    },
    "urls": {
        "Consultation_Donnees_Techniques_Contractuelles": {
            "shemaLocation": "",
            "location": ""
        },
        "Consultation_Mesures": {
            "shemaLocation": "",
            "location": ""
        },
        "Consultation_Mesure_Detaillees": {
            "shemaLocation": "",
            "location": ""
        },
        ...
    }
}

```

# Utilisation
**Initialisation**

Pour démarrer avec Zephyr SOAP Client, créez une instance du client en précisant le chemin vers le fichier de configuration si celui-ci diffère de la valeur par défaut.

```python
from zephyr_soap.SoapClient import SoapClient

# Initialisation du client SOAP
soap_client = SoapClient(config_path="SGE/Conf/settings.json")
```
**Exemples d'Utilisation des Méthodes**

```python
# Consulter les données techniques contractuelles
response = soap_client.consulter_donnees_techniques_contractuelles(pdl="98800007059999", autorisation_client=True)
print(response)

# Commander accès aux données de mesures
response = soap_client.commander_acces_donnees_mesures(pdl="24380318190106", date_debut="2024-10-31", date_fin="2026-10-30")
print(response)

# Consulter des mesures détaillées
response = soap_client.consulter_mesures_detaillees_v3(pdl='30001610071843', DateDebut="2024-01-29", DateFin="2024-01-30")
print(response)

```

# Méthodes Disponibles
- **consulter_donnees_techniques_contractuelles** : Récupère les données contractuelles et techniques.

- **commander_acces_donnees_mesures** : Commande l’accès aux données de mesures pour une période donnée.

- **commander_arret_service_souscrit_mesures** : Arrête un service souscrit pour un PDL.

- **commander_transmission_donnees_infraJ** : Commande la transmission de données infraJ pour une entreprise donnée.

- **commander_collecte_publication_mesures** : Commande la collecte et publication de mesures.

- **consulter_mesures** : Récupère les mesures d'un PDL.
- **consulter_mesures_detaillees_v3** : Récupère des mesures détaillées pour une période donnée.

- **rechercher_point** : Recherche un point de livraison en utilisant une adresse.

- **rechercher_services_souscrits_mesures** : Recherche les services souscrits pour un PDL.

- **commande_historique_donnees_mesures_fines** : Récupère l'historique des mesures fines.

- **commande_historique_donnees_mesures_facturantes** : Récupère l'historique des données de facturation.

- **commande_informations_techniques_et_contractuelles** : Récupère les informations techniques et contractuelles.

# Tests
Pour tester les méthodes, utilisez les exemples ci-dessus avec les valeurs de paramètres appropriées.


## License

Ce projet a été conçu et développé par Grâce LUSAKUMUNU DIMBU. Il est licencié sous la licence MIT. Vous pouvez consulter le fichier [LICENSE](LICENSE) pour plus d'informations sur les conditions d'utilisation.
