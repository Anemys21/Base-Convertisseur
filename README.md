# Convertisseur de bases — Anemys37

Un convertisseur de bases graphique (Tkinter) pour passer rapidement entre binaire, octal, décimal, hexadécimal et toute base de 2 à 36.

© 2025 AMOUBE NDE LOUANGE-MYSTERE

---

## Fonctionnalités

- Conversion d'entiers entre les bases 2 à 36
- Détection automatique de la base via les préfixes `0b`, `0o`, `0x`
- Affichage simultané dans les bases courantes: binaire (2), octal (8), décimal (10), hexadécimal (16)
- Choix d'une base cible personnalisée (2–36)
- Interface moderne avec thème sombre

## Prérequis

- Python 3.8 ou supérieur
- Tkinter (inclus par défaut avec Python sur Windows et macOS; sur certaines distributions Linux, installer le paquet `python3-tk`)

Vérifier la version de Python:
```bash
python --version
# ou
python3 --version
```

## Installation

1. Télécharger ou cloner ce dépôt dans un dossier local
2. Aucun paquet externe n'est requis (seulement la bibliothèque standard Tkinter)

## Exécution

Depuis le dossier du projet, exécuter:
```bash
python "Base Convertisseur.py"
# ou selon votre environnement
python3 "Base Convertisseur.py"
```

L'application démarre avec un exemple (`0xFF`).

## Utilisation

1. Saisir la valeur à convertir dans le champ « Valeur à convertir ».
   - Préfixes acceptés pour auto-détection: `0b` (binaire), `0o` (octal), `0x` (hexadécimal)
   - Exemples: `0b1010`, `0o77`, `0xFF`, `255`, `-42`
2. Choisir la « Base source »:
   - `Auto (préfixes 0b/0o/0x)` détecte si un préfixe est présent, sinon suppose décimal (10)
   - Ou sélectionner explicitement une base entre 2 et 36
3. Choisir la « Base cible » (2–36)
4. Cliquer sur « Convertir » ou appuyer sur Entrée
5. Lire les résultats dans les champs dédiés, plus la conversion dans la base cible choisie

## Bases supportées

- Entrée et sortie: bases 2 à 36
- Chiffres/lettres utilisés: `0–9` puis `A–Z` (A=10, B=11, ... Z=35)

## Limitations actuelles

- Nombres entiers uniquement (pas de fractionnaires/virgule flottante)
- Les lettres doivent être valides pour la base choisie (ex.: `G` non valide en base 16)
- Les lettres en entrée sont traitées sans sensibilité à la casse (normalisées en majuscules)

## Raccourcis et interactions

- Touche Entrée dans le champ de saisie: lance la conversion
- Changer la base source ou cible relance la conversion automatiquement

## Structure du projet

```
Convertisseur/
├─ Base Convertisseur.py   # Application Tkinter principale
└─ README.md               # Ce fichier
```

## Packager un exécutable (optionnel)

Avec `pyinstaller` (à installer au préalable):
```bash
pip install pyinstaller
pyinstaller -F -w "Base Convertisseur.py" -n Convertisseur
```
- `-F` crée un binaire unique
- `-w` masque la console (Windows/macOS)
- Le binaire se trouvera dans le dossier `dist/`

## Auteur

- AMOUBE NDE LOUANGE-MYSTERE (Anemys37)

## Licence

Projet propriétaire. Tous droits réservés, 2025.
