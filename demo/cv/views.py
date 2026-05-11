from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import CVProfile, Experience, Education, Skill, Language
from .forms import CVProfileForm, ExperienceForm, EducationForm, SkillForm, LanguageForm
from templates.models import Template as TemplateModel
import os
from django.conf import settings

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        if sRoot:
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            # Fallback to STATICFILES_DIRS if STATIC_ROOT is not set (typical in development)
            path = None
            for static_dir in settings.STATICFILES_DIRS:
                test_path = os.path.join(static_dir, uri.replace(sUrl, ""))
                if os.path.isfile(test_path):
                    path = test_path
                    break
    else:
        return uri

    # make sure that file exists
    if path and os.path.isfile(path):
        return path
    
    return uri

@login_required
def dashboard(request):
    """Affiche la liste des CVs de l'utilisateur connecté."""
    cvs = request.user.cv_profiles.all()
    return render(request, 'cv/dashboard.html', {'cvs': cvs})

@login_required
def cv_create(request):
    """Créer un nouveau profil de CV."""
    templates = TemplateModel.objects.all()
    if request.method == 'POST':
        form = CVProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            # Handle template selection manually (raw radio button in template)
            template_id = request.POST.get('template_choisi')
            if template_id:
                try:
                    cv.template_choisi = TemplateModel.objects.get(pk=template_id)
                except TemplateModel.DoesNotExist:
                    cv.template_choisi = None
            else:
                cv.template_choisi = None
            cv.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = CVProfileForm()
    return render(request, 'cv/cv_form.html', {
        'form': form,
        'title': 'Créer un nouveau CV',
        'templates': templates,
    })

@login_required
def cv_detail(request, pk):
    """Affiche les détails du CV et permet d'ajouter des sections."""
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    return render(request, 'cv/cv_detail.html', {'cv': cv})

@login_required
def cv_edit(request, pk):
    """Modifier les informations principales du profil CV."""
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    templates = TemplateModel.objects.all()
    if request.method == 'POST':
        form = CVProfileForm(request.POST, request.FILES, instance=cv)
        if form.is_valid():
            cv = form.save(commit=False)
            # Handle template selection manually
            template_id = request.POST.get('template_choisi')
            if template_id:
                try:
                    cv.template_choisi = TemplateModel.objects.get(pk=template_id)
                except TemplateModel.DoesNotExist:
                    cv.template_choisi = None
            else:
                cv.template_choisi = None
            cv.save()
            return redirect('cv_detail', pk=cv.pk)
    else:
        form = CVProfileForm(instance=cv)
    return render(request, 'cv/cv_form.html', {
        'form': form,
        'title': 'Modifier les infos du CV',
        'cv': cv,
        'templates': templates,
    })

@login_required
def cv_delete(request, pk):
    """Supprimer un profil CV complet."""
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        cv.delete()
        return redirect('cv_dashboard')
    return redirect('cv_dashboard')

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

@login_required
def generate_pdf_cv(request, pk):
    """Génère un PDF du CV à partir d'un template HTML."""
    cv = get_object_or_404(CVProfile, pk=pk, user=request.user)
    
    # Choisir le template basé sur le choix de l'utilisateur
    if cv.template_choisi:
        if 'moderne' in cv.template_choisi.nom.lower():
            template_path = 'cv/cv_pdf_moderne.html'
        elif 'classique' in cv.template_choisi.nom.lower():
            template_path = 'cv/cv_pdf_classique.html'
        else:
            template_path = 'cv/cv_pdf_moderne.html'  # Par défaut
    else:
        template_path = 'cv/cv_pdf_moderne.html'  # Par défaut si aucun template
    
    context = {'cv': cv}
    
    # Générer le PDF et le sauvegarder
    import os
    from django.conf import settings
    
    # Créer le répertoire si nécessaire
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'cv_pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    
    filename = f"cv_{cv.user.username}_{cv.pk}.pdf"
    filepath = os.path.join(pdf_dir, filename)
    
    # Trouver le template et le rendre en HTML
    template = get_template(template_path)
    html = template.render(context)
    
    # Créer le PDF dans un fichier
    with open(filepath, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file, link_callback=link_callback)
    
    # En cas d'erreur
    if pisa_status.err:
        return HttpResponse('Une erreur est survenue lors de la génération du PDF <pre>' + html + '</pre>')
    
    # Retourner la page avec le lien de téléchargement
    download_url = f"{settings.MEDIA_URL}cv_pdfs/{filename}"
    return render(request, 'cv/pdf_generated.html', {
        'cv': cv,
        'download_url': download_url,
        'filename': filename
    })
