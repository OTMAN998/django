from django.db import models

class Template(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50) # ex: 'Moderne', 'Classique'
    apercu = models.ImageField(upload_to='templates_previews/', blank=True, null=True)

    def render(self, data):
        pass

    def __str__(self):
        return self.nom
