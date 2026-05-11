from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import User
from cv.models import CVProfile
from templates.models import Template
from django import forms


def admin_required(view_func):
    """Decorator: user must be staff/admin."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_cvs': CVProfile.objects.count(),
        'total_templates': Template.objects.count(),
        'recent_users': User.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ─── Users ────────────────────────────────────────────────────────────────────

@admin_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})


@admin_required
def admin_delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('admin_users')
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"Utilisateur '{username}' supprimé avec succès.")
        return redirect('admin_users')
    return render(request, 'admin_panel/confirm_delete.html', {
        'object_type': 'utilisateur',
        'object_name': user.username,
        'cancel_url': 'admin_users',
    })


# ─── CVs ──────────────────────────────────────────────────────────────────────

@admin_required
def admin_cvs(request):
    cvs = CVProfile.objects.select_related('user', 'template_choisi').order_by('-updated_at')
    return render(request, 'admin_panel/cvs.html', {'cvs': cvs})


@admin_required
def admin_delete_cv(request, pk):
    cv = get_object_or_404(CVProfile, pk=pk)
    if request.method == 'POST':
        name = str(cv)
        cv.delete()
        messages.success(request, f"CV '{name}' supprimé.")
        return redirect('admin_cvs')
    return render(request, 'admin_panel/confirm_delete.html', {
        'object_type': 'CV',
        'object_name': str(cv),
        'cancel_url': 'admin_cvs',
    })


# ─── Templates ────────────────────────────────────────────────────────────────

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['nom', 'type', 'apercu']
        labels = {
            'nom': 'Nom du template',
            'type': 'Type (ex: Moderne, Classique)',
            'apercu': 'Image aperçu',
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Moderne Pro'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Moderne'}),
        }


@admin_required
def admin_templates(request):
    templates = Template.objects.all().order_by('nom')
    return render(request, 'admin_panel/templates_list.html', {'templates': templates})


@admin_required
def admin_template_add(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Template ajouté avec succès.")
            return redirect('admin_templates')
    else:
        form = TemplateForm()
    return render(request, 'admin_panel/template_form.html', {
        'form': form,
        'title': 'Ajouter un Template',
    })


@admin_required
def admin_template_edit(request, pk):
    template = get_object_or_404(Template, pk=pk)
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, "Template modifié avec succès.")
            return redirect('admin_templates')
    else:
        form = TemplateForm(instance=template)
    return render(request, 'admin_panel/template_form.html', {
        'form': form,
        'title': 'Modifier un Template',
        'template': template,
    })


@admin_required
def admin_template_delete(request, pk):
    template = get_object_or_404(Template, pk=pk)
    if request.method == 'POST':
        nom = template.nom
        template.delete()
        messages.success(request, f"Template '{nom}' supprimé.")
        return redirect('admin_templates')
    return render(request, 'admin_panel/confirm_delete.html', {
        'object_type': 'template',
        'object_name': template.nom,
        'cancel_url': 'admin_templates',
    })
