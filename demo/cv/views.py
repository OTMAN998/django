from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CVProfile, Experience, Education, Skill, Language
from .forms import CVProfileForm, ExperienceForm, EducationForm, SkillForm, LanguageForm

@login_required
def dashboard(request):
    """Affiche la liste des CVs de l'utilisateur connecté."""
    cvs = request.user.cv_profiles.all()
    return render(request, 'cv/dashboard.html', {'cvs': cvs})

@login_required
def cv_create(request):
    """Créer un nouveau profil de CV."""
    if request.method == 'POST':
        form = CVProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = CVProfileForm()
    return render(request, 'cv/cv_form.html', {'form': form, 'title': 'Créer un nouveau CV'})

@login_required
def cv_detail(request, pk):
    """Affiche les détails du CV et permet d'ajouter des sections."""
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    return render(request, 'cv/cv_detail.html', {'cv': cv})

@login_required
def add_experience(request, cv_id):
    cv = get_object_or_404(CVProfile, pk=cv_id, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.cvprofile = cv
            exp.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = ExperienceForm()
    return render(request, 'cv/section_form.html', {'form': form, 'cv': cv, 'title': 'Ajouter une Expérience'})

# TODO: Ajouter les vues add_education, add_skill, add_language sur le même modèle.
