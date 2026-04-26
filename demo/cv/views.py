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
def cv_edit(request, pk):
    """Modifier les informations principales du profil CV."""
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CVProfileForm(request.POST, request.FILES, instance=cv)
        if form.is_valid():
            form.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = CVProfileForm(instance=cv)
    return render(request, 'cv/cv_form.html', {'form': form, 'title': 'Modifier les infos du CV', 'cv': cv})

# ─── Expérience ────────────────────────────────────────────────────────────────

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

@login_required
def edit_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, cvprofile__user=request.user)
    cv = exp.cvprofile
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = ExperienceForm(instance=exp)
    return render(request, 'cv/section_form.html', {'form': form, 'cv': cv, 'title': 'Modifier une Expérience'})

@login_required
def delete_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, cvprofile__user=request.user)
    cv_pk = exp.cvprofile.pk
    if request.method == 'POST':
        exp.delete()
    return redirect('cv_detail', pk=cv_pk)

# ─── Formation ─────────────────────────────────────────────────────────────────

@login_required
def add_education(request, cv_id):
    cv = get_object_or_404(CVProfile, pk=cv_id, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.cvprofile = cv
            edu.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = EducationForm()
    return render(request, 'cv/section_form.html', {'form': form, 'cv': cv, 'title': 'Ajouter une Formation'})

@login_required
def edit_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, cvprofile__user=request.user)
    cv = edu.cvprofile
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            form.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = EducationForm(instance=edu)
    return render(request, 'cv/section_form.html', {'form': form, 'cv': cv, 'title': 'Modifier une Formation'})

@login_required
def delete_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, cvprofile__user=request.user)
    cv_pk = edu.cvprofile.pk
    if request.method == 'POST':
        edu.delete()
    return redirect('cv_detail', pk=cv_pk)

# ─── Compétence ──────────────────────────────────────────────────────────────

@login_required
def add_skill(request, cv_id):
    cv = get_object_or_404(CVProfile, pk=cv_id, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.cvprofile = cv
            skill.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = SkillForm()
    return render(request, 'cv/section_form.html', {'form': form, 'cv': cv, 'title': 'Ajouter une Compétence'})

@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, cvprofile__user=request.user)
    cv = skill.cvprofile
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = SkillForm(instance=skill)
    return render(request, 'cv/section_form.html', {'form': form, 'cv': cv, 'title': 'Modifier une Compétence'})

@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, cvprofile__user=request.user)
    cv_pk = skill.cvprofile.pk
    if request.method == 'POST':
        skill.delete()
    return redirect('cv_detail', pk=cv_pk)

# ─── Langue ───────────────────────────────────────────────────────────────────

@login_required
def add_language(request, cv_id):
    cv = get_object_or_404(CVProfile, pk=cv_id, user=request.user)
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.save(commit=False)
            language.cvprofile = cv
            language.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = LanguageForm()
    return render(request, 'cv/section_form.html', {'form': form, 'cv': cv, 'title': 'Ajouter une Langue'})

@login_required
def edit_language(request, pk):
    language = get_object_or_404(Language, pk=pk, cvprofile__user=request.user)
    cv = language.cvprofile
    if request.method == 'POST':
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = LanguageForm(instance=language)
    return render(request, 'cv/section_form.html', {'form': form, 'cv': cv, 'title': 'Modifier une Langue'})

@login_required
def delete_language(request, pk):
    language = get_object_or_404(Language, pk=pk, cvprofile__user=request.user)
    cv_pk = language.cvprofile.pk
    if request.method == 'POST':
        language.delete()
    return redirect('cv_detail', pk=cv_pk)
