# AGENTS.md — Assistant de compilation GitHub (APK / EXE)

Ce fichier doit être **copié à la racine du projet utilisateur**, pas laissé seulement dans la bibliothèque de templates.

## Mission

Quand l'utilisateur demande « compile », « génère APK », « crée EXE », « livre la version Windows », « mets GitHub Actions », identifier la technologie réelle et créer une chaîne de compilation reproductible. **Ne jamais annoncer un fichier APK/EXE terminé sans preuve d'un build réussi et lien vers l'artefact exact.**

## Étape 1 : diagnostic sans supposition

- Lire les fichiers à la racine, les README et dépendances. Ne pas deviner le langage.
- Flutter = `pubspec.yaml` + `lib/`. Génération Android : `flutter build apk --release`. Windows : `flutter build windows --release`.
- Android natif Kotlin/Java = `gradlew`, `app/build.gradle(.kts)`. Générer APK avec Gradle; EXE non automatique.
- Python desktop = `main.py` ou autre entrée Python, construire EXE via PyInstaller; ne pas fabriquer d'APK sans framework mobile.
- Python Flet = `pyproject.toml` avec `[tool.flet]`; étudier `flet build apk` et `flet build windows` et version du framework.
- React/Vite/Node = `package.json`; site web seul ≠ programme natif. Pour Windows, installer/configurer Tauri ou Electron d'abord. Pour Android, adapter par Capacitor/Tauri Android ou client Flutter distinct.
- Si le projet est un monorepo, détecter le répertoire exact et adapter les chemins du workflow et des artefacts.
- Exécuter `python scripts/diagnose_project.py` depuis la copie du kit, si disponible.

## Étape 2 : mettre en place GitHub Actions

1. Choisir **un** template compatible de ce kit; le copier dans `.github/workflows/` à la racine du dépôt cible.
2. Vérifier branche déclenchante (`main` par défaut), chemins, point d'entrée et dépendances verrouillées.
3. Vérifier avec lint/tests quand disponibles; corriger réellement les erreurs, ne pas masquer les échecs en `continue-on-error`.
4. Compiler sur runner adapté : Ubuntu pour Android, Windows pour EXE; l'environnement ne garantit pas les pilotes/matériels spécifiques.
5. Conserver le **dossier complet de distribution Windows** (EXE + DLL + data), pas seulement un EXE isolé pour Flutter.
6. Publier les sorties via `actions/upload-artifact` et conserver les logs.
7. Consulter les résultats de GitHub Actions et indiquer précisément statut, lien de run, artefact, erreurs.

## Étape 3 : sécurité et distribution

- **Jamais** de keystore, mots de passe, tokens, certificats, fichier `.env` sensible dans Git. Utiliser GitHub Actions Secrets si la signature est requise.
- Un APK de release n'est **pas forcément signé pour la production**; vérifier keystore propre, vérification de signature et installation réelle.
- Un EXE Windows sans certificat peut déclencher SmartScreen; signature de code distincte de la compilation.
- Vérifier droits des bibliothèques, icônes et ressources embarquées.
- Ne pas modifier la logique métier, les données clients ou les droits d'accès pour forcer un build.
- Pour réseau local/offline, tester stockage, permissions et comportement sans connexion avant remise au client.

## Critères de livraison

- Code source versionné, tests pertinents et build GitHub Actions **success**.
- APK téléchargeable pour Android avec architecture et mode de signature clairement indiqués.
- Distribution Windows téléchargeable et exécutable sur machine de test, DLL/data inclus.
- README indiquant installation, exigences Windows/Android, version, problèmes connus et procédure de mise à jour.
- En cas de blocage : expliquer **ce qui a réussi, ce qui a échoué, et la correction nécessaire**. Ne pas fabriquer d'URL ni de statut.

## Références kit

Les modèles sont dans `dev-kits/BUILD-APK-EXE/templates/` du dépôt `Stephen077j/Stephen077j`. Copier les fichiers des modèles vers la racine du dépôt de l'application avant compilation.
