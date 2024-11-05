import unittest
from unittest.mock import patch
from zephyr_soap import SoapClient

class TestSoapClient(unittest.TestCase):

    def setUp(self):
        """Initialisation de SoapClient avant chaque test."""
        self.soap_client = SoapClient()

    @patch.object(SoapClient, 'consulter_donnees_techniques_contractuelles')
    def test_consulter_donnees_techniques_contractuelles(self, mock_method):
        """Test de la méthode consulter_donnees_techniques_contractuelles."""

        res = self.soap_client.consulter_donnees_techniques_contractuelles(pdl="98800007059999", autorisation_client=True)
        self.assertEqual(res['header']['acquittement']['resultat']['code'], "SGT200")
        

#     @patch.object(SoapClient, 'commander_acces_donnees_mesures')
#     def test_commander_acces_donnees_mesures(self, mock_method):
#         """Test de la méthode commander_acces_donnees_mesures."""
      
#         res = self.soap_client.commander_acces_donnees_mesures(pdl="24380318190106", date_debut="2024-10-31", date_fin="2026-10-30")
#         self.assertEqual(res["status"], "OK")
        

#     @patch.object(SoapClient, 'commander_arret_service_souscrit_mesures')
#     def test_commander_arret_service_souscrit_mesures(self, mock_method):
#         """Test de la méthode commander_arret_service_souscrit_mesures."""

#         res = self.soap_client.commander_arret_service_souscrit_mesures(pdl="25884515170669", serviceSouscrit_Id="23051998")
#         self.assertEqual(res["status"], "OK")
        

#     @patch.object(SoapClient, 'consulter_mesures')
#     def test_consulter_mesures(self, mock_method):
#         """Test de la méthode consulter_mesures."""

#         res = self.soap_client.consulter_mesures(pdl="30001610071843", autorisation_client=True)
#         self.assertEqual(res["status"], "OK")
        

#     @patch.object(SoapClient, 'commander_collecte_publication_mesures')
#     def test_commander_collecte_publication_mesures(self, mock_method):
#         """Test de la méthode commander_collecte_publication_mesures."""

#         res = self.soap_client.commander_collecte_publication_mesures(
#             pdl="25884515170669", 
#             dateDebut="2024-10-30", 
#             dateFin="2026-12-12", 
#             denominationSociale="ZephyrENR"
#         )
#         self.assertEqual(res["status"], "OK")
        
if __name__ == '__main__':
    unittest.main()
