#!/usr/bin/env python
"""
Script pour ajouter les templates CV de base à la base de données.
Exécutez avec: python add_templates.py
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
django.setup()

from templates.models import Template

# Créer les templates s'ils n'existent pas
templates_data = [
    {
        'nom': 'Moderne',
        'type': 'Moderne',
    },
    {
        'nom': 'Classique',
        'type': 'Classique',
    },
]

for template_info in templates_data:
    template, created = Template.objects.get_or_create(
        nom=template_info['nom'],
        defaults={'type': template_info['type']}
    )
    if created:
        print(f"✓ Template '{template.nom}' créé avec succès")
    else:
        print(f"✓ Template '{template.nom}' existe déjà")

print("\nTemplates ajoutés avec succès!")
print("\nTemplates disponibles:")
for t in Template.objects.all():
    print(f"  - {t.nom} ({t.type})")
