import json
import os
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
import datetime as dt
import pytz
import sys
import logging



class SoapClient:
    def __init__(self, config_path="SGE/Conf/settings.json"):
        self.settings = self._load_settings(config_path)
        # Initialiser le logger
        self.logger = Mylogging().get_instance()
        self.logger.info("--------------------Initialisation de SoapClient-------------------")
        self.transport = self._init_transport()
        self.urls = self.settings['urls']
    
    def _load_settings(self, config_file):
        with open(config_file) as file:
            return json.load(file)

    def _init_transport(self):
        # Configuration de la session avec les certificats pour l'authentification mutuelle
        session = Session()
        connexion = self.settings['connexion']
        session.auth = HTTPBasicAuth(connexion["login"], connexion["password"])
        
        certificats = self.settings['certificats']
        session.cert = (certificats["client_cert"], certificats["client_key"])
        session.verify = certificats["ca_cert"]

        return Transport(session=session)

    def _get_timestamp(self):
        timezone = pytz.timezone('Europe/Paris')
        current_time = dt.datetime.now(timezone)
        return current_time.strftime("%d/%m/%Y %H:%M")

    def _log_request(self, service_name):
        timestamp = self._get_timestamp()
        self.logger.info(f"Heure de la demande {timestamp}")
        self.logger.info(f"demande : {service_name}")

    def _create_client(self, wsdl_path, service_url):
        client = Client(wsdl=wsdl_path, transport=self.transport)
        client.service._binding_options['address'] = service_url
        return client

    def execute_service(self, service_name, wsdl_path, url, **kwargs):
        self._log_request(service_name)
        try:
            client = self._create_client(wsdl_path, url)
            response = getattr(client.service, service_name)(**kwargs)
            return response
        except Exception as e:
            self.logger.error(f"Erreur lors de la requête SOAP : {e}")
            if hasattr(e, 'response'):
                self.logger.error(f"Contenu de la réponse : {e.response.content}")
                return e
            return e
    ###########################################
    # Méthodes spécifiques à chaque service ###
    ###########################################
    def commander_acces_donnees_mesures(self, pdl,date_debut, date_fin,type_donnees="IDX", soutirage=True,injection=False)->str:
        """
        Demande de données de mesures : `commander_acces_donnees_mesures`

        Cette fonction permet de faire une demande d'accès aux données de mesures avec les paramètres suivants :

        - **pointId** : Identifiant du point de livraison (PDL) du client.
        - **date_debut** : Date de début, qui doit correspondre à la date du jour.
        - **date_fin** : Date de fin souhaitée (doit être inférieure ou égale à 3 ans après la date de début).
        - **Type de données** : Par défaut, cette méthode récupère les données en mode "Soutirage".

        Les types de données disponibles sont les suivants :
        - **IDX** : Index.
        - **PMAX** : Puissance maximale.
        - **ENERGIE** : Consommation d'énergie.
        - **CDC** : Courbe de charge.

        Remarque : la différence entre `date_fin` et `date_debut` ne doit pas excéder 3 ans.
        """

        if soutirage == True and injection == True:
            raise Exception("Soutirage et Injection ne peuvent pas être tous deux égaux à True.")


        demande = self.__get_commander_acces_donnees_mesures_parameters()
        #donneesGenerales
        demande['donneesGenerales']['pointId'] = pdl
        #accesDonnees
        demande['accesDonnees']['typeDonnees'] = type_donnees
        demande['accesDonnees']['soutirage']   = soutirage
        demande['accesDonnees']['injection']   = injection
        #
        demande['accesDonnees']['dateDebut']   = date_debut
        demande['accesDonnees']['dateFin']     = date_fin
        # Commande_Acces_Donnees_Mesures
        return self.execute_service(
            "commanderAccesDonneesMesures",
            self.urls['Commande_Acces_Donnees_Mesures']['shemaLocation'],
            self.urls['Commande_Acces_Donnees_Mesures']['location'],
            demande=demande
        )

    #commander arret service souscrit 
    def commander_arret_service_souscrit_mesures(self, pdl,serviceSouscrit_Id):
        """
        Demande d'arrêt de service souscrit : `commander_arret_service_souscrit_mesures`
        Cette fonction permet de faire une demande pour arrêter un service souscrit aux mesures avec les paramètres suivants :
        - **pointId** : Identifiant du point de livraison (PDL) du client.
        - **serviceSouscrit_Id** : Identifiant aléatoire attribué à chaque demande.

        Remarque : Le `pointId` ne doit pas être vide.
        """

        if pdl == "":
            raise Exception("Le PDL (point de livraison) ne doit pas être vide.")

        demande = self.__get_parameters_commander_arret_service_souscrit_mesures()
        demande['donneesGenerales']['pointId'] = pdl
        demande['arretServiceSouscrit']['serviceSouscritId'] = serviceSouscrit_Id

        return self.execute_service(
            "commanderArretServiceSouscritMesures",
            self.urls['Commander_ArretService_SouscritMesures']['shemaLocation'],
            self.urls['Commander_ArretService_SouscritMesures']['location'],
            demande=demande
        )

    #commande_transmission_données_infraj
    def commander_transmission_donnees_infraJ(self, pdl,
                                              injection =False,
                                              soutirage=True,
                                              cdc=True,
                                              idx=False,
                                              ptd=True,
                                              accordClient=True,
                                              denominationSociale=""):

        """
        Paramètres de la demande :
         - **pointId** : Identifiant du point de livraison (PDL) du client.
        - **injection** : Booléen indiquant si l'injection est activée. Par défaut : `False`.
        - **soutirage** : Booléen indiquant si le soutirage est activé. Par défaut : `True`.
        - **cdc** : Booléen précisant si les données des courbes de charge et de la courbe de tension sont demandées. Par défaut : `True`.
        - **idx** : Booléen précisant si les données d’index sont demandées. Par défaut : `False`.
        - **ptd** : Booléen précisant si les données de gestion de la tarification dynamique sont demandées. Par défaut : `True`.

        Autorisations client :
        - **accordClient** : Booléen précisant si le client a donné son accord pour la collecte des données. Par défaut : `True`.
        - **injection** : Booléen indiquant si l’accord concerne les données en injection. Par défaut : `False`.
        - **soutirage** : Booléen indiquant si l’accord concerne les données en soutirage. Par défaut : `True`.
        Informations générales :
        - **denominationSociale** : Dénomination sociale de l'entreprise. Exemple : `"ZephyrENR"`.
        """

        if soutirage == True and injection == True:
            raise Exception("Soutirage et Injection ne peuvent pas être tous deux égaux à True.")
        
        if denominationSociale =="":
            raise Exception("La denomination sociale ne doit pas être vide.")

        #donneesGenerales
        demande = self.__get_parameters_commander_transmission_donnees_infraJ()
        demande['donneesGenerales']['pointId'] = pdl
        #accesDonnees
        demande['accesDonnees']['injection'] =injection
        demande['accesDonnees']['injection'] =soutirage
        demande['accesDonnees']['injection'] =cdc
        demande['accesDonnees']['injection'] =idx
        demande['accesDonnees']['injection'] =ptd

        #declarationAccordClient
        demande['accesDonnees']['declarationAccordClient']['accordClient'] =accordClient
        demande['accesDonnees']['declarationAccordClient']['injection'] =injection
        demande['accesDonnees']['declarationAccordClient']['soutirage'] =soutirage
        demande['accesDonnees']['declarationAccordClient']['personneMorale']['denominationSociale']=denominationSociale

        return self.execute_service(
            "commanderTransmissionDonneesInfraJ",
            self.urls['commander_Transmission_Donnees_InfraJ']['shemaLocation'],
            self.urls['commander_Transmission_Donnees_InfraJ']['location'],
            demande=demande
        )

    #CommanderCollectePublicationMesures
    def commander_collecte_publication_mesures(self, pdl, dateDebut,dateFin,accordCient=True,denominationSociale="",
                                               mesuresType="IDX",injection=False,soutirage=True,mesuresCorrigees=False,
                                               mesuresPas="P1D",transmissionRecurrente=True,periodiciteTransmission="P1D"):

        """
        Paramètres d'accès aux mesures (`accesMesures`) :
         - **pointId** : Identifiant du point de livraison (PDL) du client.
        - **dateDebut** : Date de début pour l'accès aux données. Elle doit être égale à la date du jour.
        - **dateFin** : Date de fin pour l'accès aux données. Pour les segments C5 et P4, la durée du service ne peut excéder trois ans à partir de la date de début.
        Déclaration d'accord client :
        - **declarationAccordClient** : Déclaration de l'accord du client pour l'accès aux données.
        - **accord** : Booléen indiquant si le client a donné son accord pour la collecte des données.
        - **personneMorale** : Informations sur la personne morale.
            - **denominationSociale** : Dénomination sociale de l'entreprise (exemple : `"ZephyrENR"`).
        Types de mesures :
        - **mesuresTypeCode** : Type de données mesurées. Les valeurs autorisées sont :
        - **"IDX"** : Données d'index.
        - **"CDC"** : Courbe de charge.
        Options de mesure :
        - **injection** : Booléen indiquant si les mesures en injection sont activées. Par défaut : `False`.
        - **soutirage** : Booléen indiquant si les mesures en soutirage sont activées. Par défaut : `True`.
        Paramètres de pas et fréquence de mesure :
        - **mesuresPas** : Pas de mesure pour la demande de transmission récurrente (valeurs possibles selon le type de données) :
        - **"P1D"** : Quotidien, pour les index quotidiens et puissances maximales quotidiennes.

        - Pour les courbes de charge :
            - **"PT10M"** : Pour C1-C4 et P1-P3 (pas de 10 minutes).
            - **"PT30M"** : Pour C5 et P4 (pas de 30 minutes).
        - **mesuresCorrigees** : Booléen indiquant si les mesures corrigées sont requises. Disponible uniquement pour les courbes de charge sur les segments C1-C4 et P1-P3. Par défaut : `False`.
        Transmission des mesures :
        - **transmissionRecurrente** : Booléen indiquant si la transmission est récurrente. Par défaut : `True`. (Pour une collecte de la courbe de charge, ce paramètre est `False`).
        - **periodiciteTransmission** : Périodicité de transmission pour les données récurrentes (obligatoire si transmission récurrente est activée).
        - Pour C1-C4 et P1-P3 : **"P1D"** (quotidienne), **"P7D"** (hebdomadaire), **"P1M"** (mensuelle).
        - Pour C5 : **"P1D"** (quotidienne), **"P1M"** (mensuelle).
        - Pour les index et données du compteur en C1-C4 et P1-P3 : uniquement **"P1D"**.
        Remarques :
        - Le paramètre `periodiciteTransmission` est ignoré en cas de demande pour une collecte de la courbe de charge.
        - La transmission récurrente des données n'est pas encore disponible pour P4, ce paramètre ne doit donc pas être inclus pour ce segment.
        """
        demande = self.get_parameters_commander_collecte_publication_mesures()
        demande['donneesGenerales']['pointId'] =pdl
        ##
        demande['accesMesures']['dateDebut'] =dateDebut
        demande['accesMesures']['dateFin'] =dateFin
        ##
        demande['accesMesures']['declarationAccordClient']['accord']=accordCient
        demande['accesMesures']['declarationAccordClient']['personneMorale']['denominationSociale']=denominationSociale
        #
        demande['accesMesures']['mesuresTypeCode']=mesuresType
        demande['accesMesures']['injection'] = injection
        demande['accesMesures']['soutirage'] = soutirage
        #mesuresCorrigees
        demande['accesMesures']['mesuresCorrigees']=mesuresCorrigees
        #mesuresPas
        demande['accesMesures']['mesuresPas']=mesuresPas
        #transmissionRecurrente
        demande['accesMesures']['transmissionRecurrente']=transmissionRecurrente
        #"periodiciteTransmission
        demande['accesMesures']['periodiciteTransmission']=periodiciteTransmission

        if soutirage == True and injection == True:
            raise Exception("Soutirage et Injection ne peuvent pas être tous deux égaux à True.")
        
        if denominationSociale =="":
            raise Exception("La denomination sociale ne doit pas être vide.")

        return self.execute_service(
            "commanderCollectePublicationMesures",
            self.urls['Commande_Collecte_Publication_Mesures']['shemaLocation'],
            self.urls['Commande_Collecte_Publication_Mesures']['location'],
            demande =demande
        )

    
    # consulter_donnees_techniques_contractuelles
    def consulter_donnees_techniques_contractuelles(self, pdl, autorisation_client=False):
        """
        Fonction : `consulter_donnees_techniques_contractuelles`
        Cette fonction permet de consulter les données techniques et contractuelles associées au point de livraison (PDL) du client.
        ### Paramètres
        - **pdl** (str) : 
        Identifiant du point de livraison du client. Il s'agit d'un code unique associé à l'installation du client pour la livraison d'électricité.
        - **autorisation_client** (bool) : 
        Indique si le client a donné son autorisation pour accéder à ses données. Ce paramètre doit être `True` pour permettre la consultation des données techniques et contractuelles.
        ### Retour
        Cette fonction retourne les données techniques et contractuelles pour le PDL fourni, sous réserve que l'autorisation du client soit validée.
        """
        if autorisation_client ==False:
            raise Exception("autorisation_client doit être `True` pour permettre la consultation des données techniques et contractuelles")
        
        return self.execute_service(
            "consulterDonneesTechniquesContractuelles",
            self.urls['Consultation_Donnees_Techniques_Contractuelles']['shemaLocation'],
            self.urls['Consultation_Donnees_Techniques_Contractuelles']['location'],
            pointId=pdl,
            loginUtilisateur=self.settings['connexion']['login'],
            autorisationClient=autorisation_client
        )
    

    def consulter_mesures(self, pdl, autorisation_client=False):

        """
        Fonction : `consulter_mesures`
        Cette fonction permet de consulter les mesures associées au point de livraison (PDL) du client, telles que les données d'index, courbes de charge, ou puissances maximales.
        ### Paramètres
        - **pdl** (str) : 
        Identifiant du point de livraison du client. C'est un code unique qui identifie l'installation du client pour la fourniture d'électricité.
        - **autorisation_client** (bool, optionnel) : 
        Booléen indiquant si le client a donné son autorisation pour accéder à ses mesures. Par défaut, cette valeur est `False`. Elle doit être `True` pour autoriser l'accès aux données de mesure.
        """
        
        if autorisation_client ==False:
            raise Exception("autorisation_client doit être `True` pour permettre la consultation des données techniques et contractuelles")
        
        return self.execute_service(
            "consulterMesures",
            self.urls['Consultation_Mesures']['shemaLocation'],
            self.urls['Consultation_Mesures']['location'],
            pointId=pdl,
            loginDemandeur=self.settings['connexion']['login'],
            contratId=self.settings['connexion']['contratId'],
            autorisationClient=autorisation_client
        )
    
    #consulter_mesures_detaillées_v3
    def consulter_mesures_detaillees_v3(self, pdl, DateDebut, DateFin,mesuresType="COURBE",
                                        grandeurPhysique="TOUT",mesuresPas="P1D",
                                        mesuresCorrigees=False,sens="SOUTIRAGE",
                                        accordClient="ACCORD_CLIENT"):
        
        """
        Paramètres pour la demande de données de mesure :
        - **pointId** : Identifiant du point de livraison (PDL) du client.
        - **mesuresTypeCode** : Type de mesure demandé.
        - Valeurs possibles :
            - **"ENERGIE"** : Mesure de l'énergie consommée.
            - **"COURBE"** : Courbe de puissance ou de tension.
            - **"PMAX"** : Puissance maximale.
            - **"INDEX"** : Index de consommation.
        - **grandeurPhysique** : Grandeur physique des mesures demandées.
        - Valeurs possibles :
            - **"TOUT"** : Pour obtenir toutes les grandeurs disponibles.
            - **"Energie"** : Liste des énergies disponibles, avec des options telles que :
            - **"EA"** : Énergie active.
            - **"ERC"** : Énergie réactive capacitive.
            - **"ERI"** : Énergie réactive inductive.
            - **'Pmax'** : Valeur de puissance maximale.
        - **dateDebut** : Date de début pour l'extraction des mesures (format : AAAA-MM-JJ). : date du jour
        - **dateFin** : Date de fin pour l'extraction des mesures (format : AAAA-MM-JJ).
        - **mesuresPas** (optionnel) : Pas de mesure, uniquement requis pour les demandes de puissance maximale.
        - Valeurs possibles :
            - **"P1D"** : Quotidien.
            - **"P1M"** : Mensuel.
        - **mesuresCorrigees** : Booléen indiquant si les mesures corrigées sont demandées. 
        - Valeur par défaut : `False`.
        - Les mesures corrigées sont disponibles uniquement pour les courbes de charge des segments C1-C4 et P1-P3.
        - **sens** : Indique la direction des mesures.
        - Valeurs possibles :
            - **"SOUTIRAGE"** : Consommation d'énergie.
            - **"INJECTION"** : Injection d'énergie dans le réseau.
        - **cadreAcces** : Cadre d'accès aux données, indiquant le type d'accord.
        - Valeurs possibles :
            - **"ACCORD_CLIENT"** : Accès basé sur l'accord du client.
            - **"SERVICE_ACCES"** : Accès fourni en tant que service.
            - **"EST_TITULAIRE"** : Accès pour le titulaire de l'accord.
        """

        Energie_types = ["EA", "ERC" ,"ERI" ]
        mesuresPasTypes = ["P1D", "P1M"]
        sensTypes =["SOUTIRAGE", "INJECTION"]

        demande = self.__get_parameters_consulter_mesures_detaillees_v3()

        match str(mesuresType).upper():
            case "PMAX":
                if str(mesuresPas).upper() in mesuresPasTypes :
                    demande["mesuresPas"] = str(mesuresPas).upper()
                else :
                    raise Exception("Valeurs possibles pour la mesuresPasTypes sont(P1D, P1M)")
                
                if str(grandeurPhysique).upper() != "PMA":
                    raise Exception("Valeurs possibles pour la grandeurPhysique est PMA")
                
            case "ENERGIE":
                if str(grandeurPhysique).upper() not in  Energie_types :
                    raise Exception("Valeurs possibles pour la grandeurPhysique sont(EA, ERC ,ERI)")
            case "COURBE":
                pass
            case "INDEX":
                pass
            case _:
                raise Exception("Valeurs possibles pour la mesuresType sont(COURBE , PMAX, ENERGIE, INDEX)")

        if str(sens).upper() not in sensTypes:
            raise Exception("les sensTypes sont(SOUTIRAGE, INJECTION)")
        
        demande['pointId'] = pdl
        demande['mesuresTypeCode']=str(mesuresType).upper()
        demande['grandeurPhysique']=str(grandeurPhysique).upper()
        demande['dateDebut']=DateDebut
        demande['dateFin']=DateFin
        demande['mesuresCorrigees']=mesuresCorrigees
        demande['sens'] =str(sens).upper()
        demande["cadreAcces"] = accordClient
            

        return self.execute_service(
            "consulterMesuresDetailleesV3",
            self.urls['Consultation_Mesure_Detaillees']['shemaLocation'],
            self.urls['Consultation_Mesure_Detaillees']['location'],
            demande=demande
        )

    #rechercher_point
    def rechercher_point(self, numeroEtNomVoie,codePostal,codeInseeCommune,rechercheHorsPerimetre=True):
        """
        Fonction : `rechercher_point`

        Cette fonction permet de rechercher un point de livraison (PDL) en fonction de l'adresse ou des codes spécifiques de localisation.
        ### Paramètres
        - **numeroEtNomVoie** (str) : 
        Numéro et nom de la voie de l'adresse (par exemple, le numéro de rue et le nom de la rue).
        - **codePostal** (str) : 
        Code postal de la commune où se situe le point de livraison.
        - **codeInseeCommune** (str) : 
        Code INSEE de la commune, utilisé pour identifier la commune de façon unique.
        - **rechercheHorsPerimetre** (bool, optionnel) : 
        Indique si la recherche doit être effectuée en dehors du périmètre géographique principal.
        - Valeur par défaut : `True`.
        - Valeurs possibles :
            - **True** : Recherche dans un périmètre élargi.
            - **False** : Recherche limitée au périmètre principal.
        ### Exemple d'utilisation
        ```python
        # Recherche d'un point de livraison avec adresse et périmètre élargi
        point = rechercher_point("10 Rue de la Paix", "75001", "75101", rechercheHorsPerimetre=True)
        """
        
        demande =self.__get_parameters_demande_rechercher_point()
        demande['adresseInstallation']["numeroEtNomVoie"] = numeroEtNomVoie
        demande['adresseInstallation']["codePostal"] =codePostal
        demande['adresseInstallation']["codeInseeCommune"] =codeInseeCommune

        demande['rechercheHorsPerimetre'] =rechercheHorsPerimetre

        return self.execute_service(
            "rechercherPoint",
            self.urls['recherhePoint']['shemaLocation'],
            self.urls['recherhePoint']['location'],
            criteres=demande,
            loginUtilisateur=self.settings['connexion']['login']
        )

    #rechercher_services_souscrits_mesures
    def rechercher_services_souscrits_mesures(self, pdl)->dict:

        """
        Fonction : `rechercher_services_souscrits_mesures`
        Cette fonction permet de rechercher les services souscrits associés aux mesures d'un point de livraison (PDL) spécifique.
        ### Paramètres
        - **pdl** (str) : 
        Identifiant du point de livraison du client. Ce code unique est utilisé pour identifier l'installation du client pour la fourniture d'électricité.
        """

        demande,login_utilisateur =  self.__get_parameters_rechercher_services_souscrits_mesures()
        demande['pointId']=pdl

        return self.execute_service(
            "rechercherServicesSouscritsMesures",
            self.urls['rechercher_Services_Souscrits_Mesures']['shemaLocation'],
            self.urls['rechercher_Services_Souscrits_Mesures']['location'],
            criteres=demande,
            loginUtilisateur=login_utilisateur
        )

    #commande_historique_donnees_mesures_facturantes
    def commande_historique_donnees_mesures_facturantes(self, pdl,dateDebut,dateFin,
                                                        sens="SOUTIRAGE",
                                                        accordClient="ACCORD_CLIENT"):
        
        """
        Paramètres pour la consultation des mesures :
        - **dateDebut** : Date de début souhaitée pour la consultation des mesures (incluse dans la plage de consultation).
        - Exemple : `"2024-01-01"`.
        - Cette date correspond généralement à la date du jour.
        - **dateFin** : Date de fin souhaitée pour la consultation des mesures (exclue de la plage de consultation).
        - Exemple : `"2024-01-31"`.
        - **format** : Format de sortie des données consultées.
        - Valeurs possibles :
            - **"JSON"** : Format JSON.
        - **sens** : Direction de la mesure pour indiquer si elle correspond à la consommation ou à l'injection d'énergie.
        - Valeurs possibles :
            - **"SOUTIRAGE"** : Consommation d'énergie.
            - **"INJECTION"** : Injection d'énergie dans le réseau.
        - **cadreAcces** : Type d'accord d'accès aux données.
        - Valeurs possibles :
            - **"ACCORD_CLIENT"** : Basé sur l'accord du client.
            - **"SERVICE_ACCES"** : Accès fourni en tant que service.
            - **"EST_TITULAIRE"** : Accès pour le titulaire de l'accord.
        - **pointId** : Liste des identifiants de points de livraison (PDL) pour lesquels les données sont demandées.
        - Peut contenir un ou plusieurs identifiants PDL, tels que `"PRM"`.
        """
        sensTypes =["SOUTIRAGE", "INJECTION"]
        cadresAcces =["ACCORD_CLIENT" , "SERVICE_ACCES","EST_TITULAIRE"]
        demande = self.__get_parameters_commande_historique_donnees_mesures_facturantes()

        demande['demande']['dateDebut']=dateDebut
        demande['demande']['dateFin']=dateFin
        demande['demande']['sens']=str(sens).upper()
        #Pour commande_historique nous n'avons pas besoin de 
        #del demande['demande']['mesuresTypeCode']
        #del demande['demande']['mesuresCorrigees']

        if str(accordClient).upper() not in  cadresAcces:
            raise Exception("Valeurs possibles pour l'accord client sont ACCORD_CLIENT , SERVICE_ACCES, EST_TITULAIRE")

        demande['demande']['cadreAcces'] =accordClient
        demande['demande']['pointIds']['pointId']=pdl

        if str(sens).upper() not in sensTypes:
            raise Exception("les sensTypes sont(SOUTIRAGE, INJECTION)")

        return self.execute_service(
            "commandeHistoriqueDonneesMesuresFacturantes",
            self.urls['CommandeHistoriqueDonneesMesuresFacturantes']['shemaLocation'],
            self.urls['CommandeHistoriqueDonneesMesuresFacturantes']['location'],
            donneesGenerales=demande['donneesGenerales'],
            demande=demande['demande']
        )
    
    #commande_historique_donnees_mesures_fines
    def commande_historique_donnees_mesures_fines(self, pdl,dateDebut,dateFin,
                                                  sens="SOUTIRAGE",mesuresType="INDEX",mesuresCorrigees=True, 
                                                  accordClient="ACCORD_CLIENT"):
        """
        Paramètres pour la consultation des mesures :
        - **dateDebut** : Date de début souhaitée pour la consultation des mesures (incluse dans la plage de consultation).
        - Exemple : `"2024-01-01"`.
        - Cette date correspond généralement à la date du jour.
        - **dateFin** : Date de fin souhaitée pour la consultation des mesures (exclue de la plage de consultation).
        - Exemple : `"2024-01-31"`.
        - **format** : Format de sortie des données consultées.
        - Valeurs possibles :
            - **"JSON"** : Format JSON.
        - **sens** : Direction de la mesure pour indiquer si elle correspond à la consommation ou à l'injection d'énergie.
        - Valeurs possibles :
            - **"SOUTIRAGE"** : Consommation d'énergie.
            - **"INJECTION"** : Injection d'énergie dans le réseau.
        - **mesuresTypeCode** : Type de mesure demandé.
        - Valeurs possibles :
            - **"INDEX"** : Index de consommation.
            - **"ENERGIE"** : Mesure de l'énergie.
            - **"PMAX"** : Puissance maximale.
            - **"COURBES"** : Courbes de charge ou de tension.
        - **mesuresCorrigees** : Indicateur pour recevoir des données corrigées (uniquement disponible pour certains types de mesures).
        - Valeur par défaut : `True`.
        - **cadreAcces** : Type d'accord d'accès aux données.
        - Valeurs possibles :
            - **"ACCORD_CLIENT"** : Basé sur l'accord du client.
            - **"SERVICE_ACCES"** : Accès fourni en tant que service.
            - **"EST_TITULAIRE"** : Accès pour le titulaire de l'accord.
        - **pointId** : Liste des identifiants de points de livraison (PDL) pour lesquels les données sont demandées.
        - Peut contenir un ou plusieurs identifiants PDL, tels que `"PRM"`.
        """
        sensTypes =["SOUTIRAGE", "INJECTION"]
        mesuresTypeCode = ["INDEX", "ENERGIE","PMAX","COURBES"]

        demande = self.__get_parameters_commande_historique_donnees_mesures_fine()

        demande['demande']['dateDebut']=dateDebut
        demande['demande']['dateFin']=dateFin
        demande['demande']['sens']=str(sens).upper()
        demande['demande']['mesuresTypeCode']=str(mesuresType).upper()
        demande['demande']['mesuresCorrigees']=mesuresCorrigees

        demande['demande']['cadreAcces'] =accordClient
        demande['demande']['pointIds']['pointId']=pdl

        if str(mesuresType).upper() not in mesuresTypeCode:
            raise Exception("Les valeurs possibles pour  mesuresType sont(INDEX, ENERGIE,PMAX,COURBES) ")

        if str(sens).upper() not in sensTypes:
            raise Exception("les sensTypes sont(SOUTIRAGE, INJECTION)")

        return self.execute_service(
            "commandeHistoriqueDonneesMesuresFines",
            self.urls['commande_Historique_Donnees_Mesures_Fines']['shemaLocation'],
            self.urls['commande_Historique_Donnees_Mesures_Fines']['location'],
            donneesGenerales=demande['donneesGenerales'],
            demande=demande['demande']
        )
    
    #commande_informations_techniques_et_contractuelles
    def commande_informations_techniques_et_contractuelles(self, pdl,sens="SOUTIRAGE",
                                                           accordClient="ACCORD_CLIENT"):
        """
        Fonction : `commande_informations_techniques_et_contractuelles`

        Cette fonction permet de récupérer les informations techniques et contractuelles pour un point de livraison (PDL) spécifique, en précisant le sens de la mesure et le cadre d'accès autorisé.

        ### Paramètres
        - **pdl** (str) : 
        Identifiant unique du point de livraison (PDL) du client, qui permet de cibler l'installation spécifique.
        Peut contenir un ou plusieurs identifiants PDL, tels que 
        - **sens** (str, optionnel) : 
        Direction de la mesure pour laquelle les informations sont demandées.
        - Valeur par défaut : `"SOUTIRAGE"`.
        - Valeurs possibles :
            - **"SOUTIRAGE"** : Consommation d'énergie.
            - **"INJECTION"** : Injection d'énergie dans le réseau.
        - **accordClient** (str, optionnel) : 
        Cadre d'accès aux informations techniques et contractuelles.
        - Valeur par défaut : `"ACCORD_CLIENT"`.
        - Valeurs possibles :
            - **"ACCORD_CLIENT"** : Basé sur l'accord du client.
            - **"SERVICE_ACCES"** : Accès fourni en tant que service.
            - **"EST_TITULAIRE"** : Accès pour le titulaire de l'accord.
        ### Retour
        Cette fonction retourne les informations techniques et contractuelles associées au PDL fourni, en fonction du sens et du cadre d'accès spécifiés.
        ### Exemple d'utilisation
        ```python
        # Récupération des informations techniques et contractuelles pour un PDL donné
        infos = commande_informations_techniques_et_contractuelles([2345678901234], sens="INJECTION", accordClient="SERVICE_ACCES")

                
        """
        sensTypes =["SOUTIRAGE", "INJECTION"]
       

        demande = self.__get_parameters_commande_historique_donnees_mesures_fine()

        del demande['demande']['dateDebut']
        del demande['demande']['dateFin']

        demande['demande']['sens']=str(sens).upper()
        del demande['demande']['mesuresTypeCode']
        del demande["demande"]['mesuresCorrigees']
        
        demande['demande']['cadreAcces'] =accordClient
        demande['demande']['pointIds']['pointId']=pdl

       
        if str(sens).upper() not in sensTypes:
            raise Exception("les sensTypes sont(SOUTIRAGE, INJECTION)")
        
        return self.execute_service(
            "commandeInformationsTechniquesEtContractuelles",
            self.urls['Commande_Informations_Techniques_Et_Contractuelles']['shemaLocation'],
            self.urls['Commande_Informations_Techniques_Et_Contractuelles']['location'],
            donneesGenerales=demande['donneesGenerales'],
            demande=demande['demande']
        )

    ######################################################
    ################# getters  parameters          #######
    ######################################################

    def __get_commander_acces_donnees_mesures_parameters(self):
        return {
            'donneesGenerales': {
                #'refExterne': ref_Externe,
                'objetCode': 'AME', # Enedis catalogue
                'pointId': "",
                'initiateurLogin': self.settings['connexion']['login'],
                'contrat': {
                    'contratId': self.settings['connexion']['contratId'],
                    'acteurMarcheCode': 'AM',
                    'contratType': 'GRD-F' #Falcultatif voir dans Enedis catalogue
                }
            },
            'accesDonnees': {
                'dateDebut': "", 
                'dateFin': "",
                'declarationAccordClient': {
                    'accord': True,
                },
                'typeDonnees': 'IDX', #IDX ? PMAX ,ENERGIE,CDC
                'soutirage': True,
                'injection': False
            }
        }
    
    def __get_parameters_commander_arret_service_souscrit_mesures(self):
        return {
            'donneesGenerales': {
                # "refFrn":"",
                "objetCode":"ASS",
                "pointId":"",
                "initiateurLogin":self.settings['connexion']['login'],
                "contratId":self.settings['connexion']['contratId']    
            },
            'arretServiceSouscrit': {
                "serviceSouscritId":""
            }
        }

    def __get_parameters_commander_transmission_donnees_infraJ(self):
        return {
            'donneesGenerales': {
                # "refFrn":"",
                "objetCode":"AME",
                "pointId":"",
                "initiateurLogin":self.settings['connexion']['login'],
                "contratId":self.settings['connexion']['contratId']     
            },
            'accesDonnees': {
                "injection" :False,
                "soutirage" :True,
                "cdc" :True,  #Précise si les données des courbes de charge et de la courbe de tension sont demandées
                "idx" :False, #Précise si les données d’index sont demandées 
                "ptd":True, #Précise si les données de gestion de la tarification dynamique sont demandées
                "declarationAccordClient":{
                    "accordClient" :True,
                    "injection" :False, #Booléen précisant s’il s’agit d’une déclaration d’accord sur les données en injection
                    "soutirage":True,  #Booléen précisant s’il s’agit d’une déclaration d’accord sur les données en soutirage
                    "personneMorale":{
                        "denominationSociale":""
                    }
                    
                }
            }
        }
    def get_parameters_commander_collecte_publication_mesures(self):
        return {
            "donneesGenerales": {
                #"refExterne":"", Facultatif
                "objetCode": "AME",
                "pointId": "",  
                "initiateurLogin": self.settings['connexion']['login'],
                "contratId": self.settings['connexion']['contratId']
            },
            "accesMesures": {
                "dateDebut": "", 
                "dateFin": "",           
                "declarationAccordClient": {
                    "accord": True,
                    "personneMorale": {
                        "denominationSociale": ""
                    }
                },
                "mesuresTypeCode": "IDX",  
                "injection": False,
                "soutirage": True,
                "mesuresPas": "P1D",
                "mesuresCorrigees": False, 
                "transmissionRecurrente": True, 
                "periodiciteTransmission": "P1D"
            }
        }


    def __get_parameters_consulter_mesures_detaillees_v3(self):
        return  {
            "initiateurLogin" : self.settings['connexion']['login'],  
            "pointId" :"",  
            "mesuresTypeCode":"ENERGIE",  
            "grandeurPhysique":"ERI",  
            "dateDebut":"",  
            "dateFin":"",  
            "mesuresCorrigees":False,   
            "sens":"SOUTIRAGE",  
            "cadreAcces":"ACCORD_CLIENT"  
        }



    def __get_parameters_rechercher_services_souscrits_mesures(self):
        return {
            "pointId": "", 
            "contratId": self.settings['connexion']['contratId']
        },self.settings['connexion']['login']

    def __get_parameters_commande_historique_donnees_mesures_fine(self):
        return {
            'donneesGenerales': {
                "initiateurLogin":self.settings['connexion']['login'],
                "contratId":self.settings['connexion']['contratId'],
            },
            "demande":{
                "dateDebut":"", 
                "dateFin":"", 
                "format":"JSON",
                "sens":"SOUTIRAGE",
                "mesuresTypeCode" :"INDEX", 
                "mesuresCorrigees":True, 
                "cadreAcces":"ACCORD_CLIENT", 
                "pointIds":{
                    "pointId":[]
                }
            }
            
        }
    def __get_parameters_commande_historique_donnees_mesures_facturantes(self):
        return{
            'donneesGenerales': {
                "initiateurLogin":self.settings['connexion']['login'],
                "contratId":self.settings['connexion']['contratId'],
            },
            "demande":{
                "dateDebut":"", 
                "dateFin":"", 
                "format":"JSON",
                "sens":"SOUTIRAGE",  
                "cadreAcces":"ACCORD_CLIENT", 
                "pointIds":{
                    "pointId":[]

                }
            }
        
        }


    def __get_parameters_demande_rechercher_point(self):
        return {
            "adresseInstallation": {
                "numeroEtNomVoie": "", 
                "codePostal":  "",
                "codeInseeCommune":""
            },
            "rechercheHorsPerimetre": True  
    
        }



class Mylogging:
    def __init__(self) -> None:
        self.logFormatter = logging.Formatter(fmt='%(asctime)s :: %(name)s :: %(levelname)-8s :: %(message)s')
        # Dossier où mettre tous les logs
        self.directoryLog = "dataLog"
        self.create_directory(self.directoryLog)
        self.logger = self.setup_logger('log', 'log.log')
        
        # self.logger.info("Initialize finish")

    def create_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully!")

    def setup_logger(self, name, logFile, level=logging.INFO):
        # Changez le mode de 'w' à 'a' pour ajouter au fichier
        handler = logging.FileHandler(os.path.join(self.directoryLog, logFile), mode='a')        
        handler.setFormatter(self.logFormatter)

        # Créer le logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        # Ajouter le handler au logger
        logger.addHandler(handler)

        return logger
    
    def get_instance(self):
        return self.logger
