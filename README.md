# 📄 CV Generator — Application Django

Un générateur de CV en ligne développé avec Django 6, permettant aux utilisateurs de créer, personnaliser et gérer leurs CVs de manière simple et intuitive.

---

## 🚀 Fonctionnalités

- **Authentification complète** : Inscription, connexion, déconnexion, vérification par email, et réinitialisation de mot de passe.
- **Gestion de profil CV** : Créer et personnaliser son profil (photo, poste, adresse, LinkedIn).
- **Sections dynamiques** : Ajouter, modifier et supprimer :
  - 💼 Expériences professionnelles
  - 🎓 Formations & Diplômes
  - 🛠️ Compétences (avec barre de progression)
  - 🌍 Langues
- **Tableau de bord** : Vue d'ensemble de tous les CVs de l'utilisateur.
- **Interface moderne** : Design Glassmorphism avec Bootstrap 5.
- **Génération PDF** *(à venir)*.

---

## 🏗️ Architecture du Projet

Le projet est organisé en applications Django modulaires :

```
demo/
├── accounts/        # Authentification & gestion utilisateurs
├── cv/              # Profils CV et sections (expériences, formations, etc.)
├── generator/       # Service de génération de CV (PDF)
├── templates/       # Modèles de CV (template designs)
└── demo/            # Configuration principale du projet
```

---

## ⚙️ Technologies Utilisées

| Technologie | Version | Rôle |
|---|---|---|
| Python | 3.14 | Langage principal |
| Django | 6.0.4 | Framework web |
| MySQL | 8+ | Base de données |
| Bootstrap | 5 | Interface utilisateur |
| django-crispy-forms | latest | Rendu des formulaires |
| crispy-bootstrap5 | latest | Pack Bootstrap 5 pour crispy |

