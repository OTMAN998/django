class PDFGenerator:
    """
    Classe de service pour la génération de CV en PDF.
    Utilise ReportLab (ou WeasyPrint) côté serveur.
    """
    def __init__(self, template_choisi, data):
        self.template_choisi = template_choisi
        self.data = data

    def generate(self, cvprofile):
        """
        Génère le PDF à partir d'un objet CVProfile.
        """
        pass

    def apply_template(self):
        """
        Applique les styles du template choisi.
        """
        pass

    def download(self):
        """
        Génère la réponse HTTP pour télécharger le PDF.
        """
        pass
