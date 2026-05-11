from django import forms
from django.forms.widgets import ClearableFileInput
from .models import CVProfile, Experience, Education, Skill, Language

class CustomFileInput(ClearableFileInput):

    initial_text = ''
    input_text = 'Choisir une photo'
    clear_checkbox_label = ''
    
    
class CVProfileForm(forms.ModelForm):
    class Meta:
        model = CVProfile
        fields = ['titre_poste', 'description', 'photo', 'adresse', 'linkedin']
        labels = {
            'titre_poste': 'Titre du poste',
            'description': 'Résumé professionnel / À propos',
            'photo': 'Photo',
            'adresse': 'Adresse',
            'linkedin': 'LinkedIn',
        }
        widgets = {
            'photo': CustomFileInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Présentez-vous en quelques lignes...'}),
            'adresse': forms.Textarea(attrs={'rows': 2}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['poste', 'entreprise', 'date_debut', 'date_fin', 'description']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['diplome', 'etablissement', 'annee', 'mention']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['nom', 'niveau']
        widgets = {
            'niveau': forms.NumberInput(attrs={'type': 'number', 'min': 0, 'max': 100}),
        }

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['langue', 'niveau']
        widgets = {
            'langue': forms.Select(attrs={'class': 'form-select'}),
            'niveau': forms.Select(attrs={'class': 'form-select'}),
        }
