# 🚀 BUILD FACTORY — APK Android + EXE Windows dans GitHub

**Créé pour des développeurs Flutter, Python, React/Tauri et Android natif.**

> 💡 **En 1 seconde :** code source GitHub → Actions → compilation Linux/Windows → **APK ou EXE à télécharger**. Les workflows sont **des modèles à copier** dans chaque dépôt d'application; ils ne compilent rien lorsqu'ils restent rangés dans ce dossier de documentation.

## ⚡ Choisir le modèle immédiatement

| Ton projet | Fichiers à reconnaître | Modèle à copier | Résultat GitHub Actions |
|---|---|---|---|
| 📱 + 🖥️ **Flutter** | `pubspec.yaml`, `lib/main.dart`, `android/`, `windows/` | [Flutter APK + EXE](templates/flutter/.github/workflows/build-apk-exe.yml) | APK Android **et** dossier Windows avec EXE + DLL/data |
| 🐍 **Python desktop** | `main.py`, éventuellement `requirements.txt` | [Python EXE](templates/python-desktop/.github/workflows/build-python-exe.yml) | EXE Windows via PyInstaller |
| 🌐 **React + Vite + Tauri** | `package.json`, `pnpm-lock.yaml`, `src-tauri/` | [Tauri Windows](templates/tauri-windows/.github/workflows/build-tauri-windows.yml) | Installateur Windows EXE/MSI selon Tauri |
| 🤖 **Android Kotlin/Java** | `gradlew`, `app/build.gradle` ou `.kts` | [Android natif](templates/android-native/.github/workflows/build-kotlin-apk.yml) | APK **debug** Android (test, pas production) |
| 🧠 **Flet Python** | `pyproject.toml` avec `[tool.flet]` | Adapter [Flet Build Action](https://github.com/flet-dev/flet-build-action) | Potentiellement APK + Windows, selon configuration |
| 🌍 **Simple site React/PHP/Django** | `package.json`, `.php`, `manage.py` | **Aucun convertisseur magique** | Ajouter une vraie cible native adaptée |

**Agent IA :** copier aussi [AGENTS.md](templates/AGENTS.md) à la racine du projet pour guider Copilot/Codex/Claude selon leur support. **Diagnostic :** [diagnose_project.py](scripts/diagnose_project.py).

## 🏁 Démarrage rapide — Flutter (APK + EXE)

**À faire dans le dépôt de TON application Flutter** :

1. Vérifier la présence de `pubspec.yaml`, `lib/main.dart`, `android/`, `windows/`. Si Windows manque, dans un environnement avec Flutter, exécuter `flutter create --platforms=windows .` puis versionner les fichiers. Idem pour Android : `flutter create --platforms=android .`.
2. Créer un dossier `.github/workflows/` **à la racine de ton projet**.
3. Copier le fichier **[build-apk-exe.yml](templates/flutter/.github/workflows/build-apk-exe.yml)** dedans, en conservant le nom `build-apk-exe.yml`.
4. Copier [AGENTS.md](templates/AGENTS.md) à la racine (optionnel, mais utile avec les assistants IA).
5. Envoyer tes changements sur la branche `main` de ton projet. Si ta branche principale porte un autre nom, changer `branches: [main]` dans le workflow.
6. Ouvrir ton dépôt GitHub → **Actions** → **BUILD | Android APK + Windows EXE (Flutter)** → une exécution → télécharger **Android-APK-release** et **Windows-EXE-et-dependances** après réussite.

**GitHub Actions peut également démarrer via le bouton « Run workflow » lorsque le workflow est enregistré sur la branche par défaut et que les Actions sont autorisées.**

### Comment utiliser les fichiers

- Android : télécharger l'artefact `Android-APK-release`, décompresser le ZIP d'artefact GitHub et installer le `.apk` sur téléphone compatible.
- Windows : télécharger `Windows-EXE-et-dependances`, **décompresser tous les fichiers**, puis exécuter l'EXE dans le même dossier que les DLL et `data/`.
- Aucun `APK` ni `EXE` n'est fourni par le kit lui-même : **il faut y ajouter le véritable code du projet et obtenir un build réussi**.
- En cas d'échec de `flutter analyze` ou des tests, corriger le code avant la compilation. Les plugins mobiles peuvent ne pas prendre en charge Windows.

### Commandes localement (facultatives)

```bash
flutter pub get
flutter analyze
flutter test
flutter build apk --release
```

Windows : `flutter build windows --release`.

## 🧭 Démarrage Python desktop

Copier [build-python-exe.yml](templates/python-desktop/.github/workflows/build-python-exe.yml) vers `.github/workflows/build-python-exe.yml` de ton projet Python. Le modèle suppose **main.py** comme point d'entrée, à adapter si différent; il installe `requirements.txt` puis PyInstaller sur un runner Windows.

⚠️ Un programme console Python devient un EXE console; pour une vraie interface desktop, il faut du code GUI (Tkinter, PySide, etc.). Les données et ressources doivent être incluses dans le paquet si utilisées.

## 🌆 Démarrage React/Vite

Un site React + Vite est une **application web**. Pour le distribuer comme EXE Windows, il faut l'initialiser avec Tauri ou Electron. Le modèle [Tauri](templates/tauri-windows/.github/workflows/build-tauri-windows.yml) suppose que Tauri **existe déjà**, que `pnpm-lock.yaml` est versionné et que `pnpm exec tauri build` fonctionne. Il ne crée pas de projet Tauri à partir de zéro. Pour APK Android, il faut un flux séparé (Capacitor ou adaptation mobile réelle).

## 🧪 Démarrage Android natif

Le modèle Gradle produit un **APK debug de test** en faisant `./gradlew :app:assembleDebug`. La distribution client exige un **APK release signé avec ta propre clé**, une procédure distincte.

## 🔐 À ne jamais oublier

1. **Signature Android :** `flutter build apk --release` compile en mode release, mais ne garantit pas une **signature commerciale personnelle**. Configurer une clé de signature (keystore), les variables/secrets GitHub et Gradle avant de distribuer en production. Ne jamais publier la clé ni les mots de passe.
2. **Signature Windows :** sans signature de code, Windows SmartScreen peut afficher un avertissement; un EXE compilé n'est pas automatiquement certifié.
3. **GitHub Actions :** autoriser Actions dans les paramètres du dépôt; vérifier limites d'utilisation, quotas et permissions selon le plan.
4. **Mono-repo :** adapter `working-directory`, chemins d'artefacts et emplacement des fichiers Flutter/Tauri.
5. **Versions :** utiliser Flutter stable au départ; ensuite figer une version de Flutter/Java/Node/Rust validée avec ton projet pour éviter les changements imprévus.
6. **Tests réels :** tester APK sur le téléphone cible et distribution Windows sur un PC propre, sans outil de développement.
7. **Déploiement :** artefacts Actions ≠ publication Google Play ou installation signée Windows. Le déploiement commercial est une étape supplémentaire.

## 🤖 Diagnostic automatique

Télécharger ou copier [scripts/diagnose_project.py](scripts/diagnose_project.py), puis exécuter :

```bash
python scripts/diagnose_project.py /chemin/vers/mon-projet
```

Le script identifie Flutter, Python, Tauri, Flet, Android natif et React quand il reconnaît leurs fichiers. **Il n'exécute pas le projet, ne modifie pas de code, et peut demander une vérification manuelle**.

## ✅ Statuts exacts

- **KIT PRÊT** : modèles YAML et documentation créés dans le dépôt.
- **BUILD NON TESTÉ** : aucun projet applicatif n'a été fourni à ce kit. Aucun APK ni EXE réel généré pour ce kit.
- **PORTABLE** : modèles à copier et ajuster selon chaque technologie; un modèle n'est pas universel.
- **REVUE RECOMMANDÉE** : faire un premier test GitHub Actions dans le dépôt cible avant de confier une application à un client.

Créé par la bibliothèque de développement du compte GitHub **Stephen077j**. Les bibliothèques et actions tierces conservent leurs propres licences.

## Sources officielles

- [Flutter Android](https://docs.flutter.dev/deployment/android)
- [Flutter desktop](https://docs.flutter.dev/platform-integration/desktop)
- [GitHub Actions Artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts)
- [Tauri Windows](https://v2.tauri.app/distribute/windows-installer/)
- [Flet Build Action](https://github.com/flet-dev/flet-build-action)
