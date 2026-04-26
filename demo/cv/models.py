from django.db import models
from templates.models import Template
from django.conf import settings

class CVProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cv_profiles')
    titre_poste = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='cv_photos/', blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    template_choisi = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True, related_name='cvs')

    def generate_pdf(self):
        pass

    def __str__(self):
        return f"CV de {self.user.username} - {self.titre_poste}"

# --- Classes de Sections de CV ---

class CVSection(models.Model):
    cvprofile = models.ForeignKey(CVProfile, on_delete=models.CASCADE, related_name='%(class)ss')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Experience(CVSection):
    poste = models.CharField(max_length=150)
    entreprise = models.CharField(max_length=150)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    description = models.TextField()

class Education(CVSection):
    diplome = models.CharField(max_length=150)
    etablissement = models.CharField(max_length=150)
    annee = models.IntegerField()
    mention = models.CharField(max_length=50, blank=True, null=True)

class Skill(CVSection):
    nom = models.CharField(max_length=100)
    niveau = models.IntegerField(help_text="Niveau de 1 à 100 par exemple")

class Language(CVSection):
    langue = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50, help_text="Ex: A1, B2, Courant")
