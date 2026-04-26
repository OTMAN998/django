from django import forms
from .models import CVProfile, Experience, Education, Skill, Language

class CVProfileForm(forms.ModelForm):
    class Meta:
        model = CVProfile
        fields = ['titre_poste', 'photo', 'adresse', 'linkedin', 'template_choisi']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
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
            'niveau': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['langue', 'niveau']
