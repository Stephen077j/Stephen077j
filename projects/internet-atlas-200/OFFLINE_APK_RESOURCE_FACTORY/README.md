# 📱💎 OFFLINE APK RESOURCE FACTORY 2026
## 120 ressources • 30 domaines • kits de préparation pour applications Android sans Internet

**En 1 seconde :** je choisis le type d'application → je vois les assets/moteurs utiles → je génère mon dossier de préparation → je vérifie les droits et la présence des fichiers → je les intègre au vrai projet → je compile l'APK.

> **État :** 120 liens catalogués, 30 domaines, script Python de génération de kits **publié**. Les fichiers tiers ne sont pas téléchargés ni redistribués. Ce n'est pas une application APK compilée, un inventaire de 120 licences vérifiées ou un audit de compatibilité.

### ⚡ Quel type de travail ? Quoi récupérer ?

| Type d'APK | Ressources indispensables | Chercher dans le CSV |
|---|---|---|
| 🎮 Jeux 2D/3D | sprites, personnages, tilesets, bruitages, moteur, sauvegardes | Assets de jeux 2D/3D · Moteurs de jeux |
| 🎤 Karaoké / chants | fichiers audio **autorisés**, paroles **autorisées**, lecteur local, recherche, playlists | Musiques et chants · Lecteurs audio |
| 🎛️ Studio musical | enregistreur, codecs, formes d'onde, mixage, instruments, exports | Studio musical et mixage · Sons et bruitages |
| 🎬 Montage vidéo | FFmpeg/Media3, effets, polices, transition, bibliothèque média, export | Création et montage vidéo · Animation et interfaces |
| 📸 Photo / collage | filtres, retouche, stickers, fonts, cadres, sauvegarde | Retouche photo et graphiques · Images et illustrations |
| 🧑‍🏫 École / université | cours, exercices, quiz, fichiers, SQLite, résultats, recherches | Études et cours hors ligne · Contenus éducatifs |
| 📚 Livres / dictionnaires | textes libres de droits, corpus, index local, moteur de recherche | Langues et dictionnaires · Contenus éducatifs |
| 🧾 Factures / devis | PDF, logos, polices, base SQLite, numérotation, export | PDF, formulaires et facturation · Base de données locale |
| 🛒 POS / boutique | scanner codes-barres, tickets 58mm, imprimante, stocks, audit | Caisse, POS et imprimantes · ERP, gestion et administration |
| 🏨 Hôtel / réservation | calendrier, ressources locales, reçus, permissions, disponibilité | ERP, gestion et administration · Synchronisation éventuelle / LAN |
| 🧠 IA embarquée | runtime ONNX/LiteRT, poids de modèles sous licence, RAM suffisante | Moteurs IA locale · IA et reconnaissance vocale |
| 🎙️ Transcription / lecture vocale | modèle local STT/TTS, microphone, permissions, langue | IA et reconnaissance vocale |
| 📄 Scanner et OCR | OCR, modèles langues, caméra, stockage, export PDF | OCR, scanner et documents · PDF, formulaires et facturation |
| 🗺️ Voyage / GPS | données cartographiques offline autorisées, itinéraires, GPS | Cartographie, GPS et voyage |
| 🌾 Agriculture | formulaires GPS, parcelles, données cultures/sols, base locale | Agriculture et relevés terrain |
| 🏥 Santé / nutrition | données médicales protégées, formulaires, chiffrement, profils | Santé et nutrition · Chiffrement et sauvegarde |
| 💬 Messages entre téléphones | Wi-Fi local/Bluetooth, découverte appareils, stockage | Réseau local et Bluetooth |
| 📋 Enquêtes / formulaires | champs, règles de validation, caméra, GPS, export CSV | Agriculture et relevés terrain · Base de données locale |
| 🔐 Coffre-fort / notes privées | base chiffrée, biométrie si disponible, sauvegarde locale | Chiffrement et sauvegarde |
| 🎨 Design et UI premium | SVG, typographies, animations, illustrations sous licence | Icônes UI · Polices et émojis · Animation et interfaces |

**Catalogue complet :** [RESOURCES_120.csv](RESOURCES_120.csv) — pour chaque lien : domaine, besoin du pack, source, URL, utilité immédiate, mode de fonctionnement offline, risque/licence et statut de vérification.

### 📂 Utiliser le générateur de kit sans Internet

Il suffit de cloner ou télécharger **ce dossier** depuis GitHub puis d'exécuter Python 3.10+ :

```bash
python scripts/prepare_offline_kit.py --list
python scripts/prepare_offline_kit.py --domain "Musiques et chants" --out mon_kit_chansons
python scripts/prepare_offline_kit.py --domain "Assets de jeux 2D/3D" --out mon_kit_jeu
python scripts/prepare_offline_kit.py --domain "Création et montage vidéo" --out mon_kit_video
```

Cela crée **sans aucun téléchargement réseau** :

```text
mon_kit_chansons/
├── README.md                # sources et utilité expliquées
├── OFFLINE_CHECKLIST.md     # tests à faire sur le vrai téléphone
├── assets-manifest.json     # provenance + droit de chaque fichier
└── assets/
    ├── icons/    fonts/    images/    sprites/    animations/
    ├── audio/    music/    video/     models/     datasets/
    └── maps/     documents/ other/
```

Les dossiers restent vides jusqu'à ce que **tu ajoutes toi-même des fichiers autorisés**. Dans `assets-manifest.json`, remplace l'exemple par les fichiers réellement présents, leur source, licence et empreinte éventuelle.

Puis :

```bash
python scripts/prepare_offline_kit.py --audit mon_kit_chansons
```

Ce contrôle signale les assets absents, les chemins dangereux, les références manquantes et les licences **non déclarées**. **Il ne certifie pas juridiquement qu'une licence est valide** et ne teste pas la qualité des moteurs. Le champ `redistribution_allowed=VERIFIED_BY_USER` reste une déclaration de la personne qui vérifie réellement le droit.

### ✅ 10 vérifications avant un APK vraiment hors ligne

1. Le cœur de l'application doit marcher **dès la première ouverture en mode avion**, pas seulement après une connexion initiale.
2. La base SQLite/Room/Drift et les ressources essentielles sont disponibles localement.
3. Aucun CDN, font distant, compte cloud obligatoire, licence serveur ou paiement en ligne n'est requis pour le cœur de l'usage.
4. Les poids IA, voix, cartes, vidéos et bases volumineuses peuvent être livrés via un pack initial préinstallé ou une importation USB/SD **si les droits l'autorisent**.
5. Toutes les licences sont conservées (moteur, modèles, images, sons, polices, livres, paroles).
6. Les icônes et illustrations sont compressées sans dégrader la qualité; optimiser taille de l'APK et RAM.
7. Les sauvegardes/export/import sont fonctionnels sans réseau.
8. Les permissions Android sont limitées aux fonctionnalités présentes.
9. Les tests incluent redémarrage, stockage plein, permissions refusées et téléphone peu puissant.
10. Les builds Android release sont signés avec une clé appropriée, sans mettre les secrets sur GitHub.

### ⚠️ Les pièges importants en novembre 2026

- **Kenney :** ses assets publiés sur les pages de ressources sont indiqués CC0. [FAQ officielle](https://kenney.nl/support).
- **Quaternius :** attention aux anciennes pages parlant de CC0 : sa [licence officielle actualisée au 28/08/2026](https://quaternius.com/license.html) est la **QAL v1.0**, autorisant l'intégration à des produits mais interdisant la redistribution autonome de packs.
- **Freesound :** CC0, CC BY et CC BY-NC selon le son. Ne pas sélectionner automatiquement les pistes CC BY-NC pour un jeu ou une application vendus. [FAQ](https://freesound.org/help/faq/).
- **Mixkit :** les **effets sonores** peuvent être intégrés à des jeux dans les conditions publiées; la licence des **musiques** interdit notamment leur usage dans les jeux vidéo. [Conditions SFX](https://mixkit.co/license/modal/sfxFree/) · [Conditions musique](https://mixkit.co/license/modal/musicFree/).
- **PhET :** licence courante **CC BY-NC 4.0**; l'incorporation commerciale requiert une autorisation distincte. [Licence](https://phet.colorado.edu/in/licensing).
- **OpenStax :** son aide actuelle indique **CC BY-NC-SA** pour les manuels; ne pas présumer qu'un livre est réutilisable dans une application payante sans contrôler sa version et demander la permission si nécessaire. [Aide licence](https://help.openstax.org/s/article/Licensing-information-of-OpenStax-textbooks).
- **FFmpeg :** le régime LGPL/GPL dépend des composants activés et de la façon de redistribuer l'application. [FFmpeg Legal](https://ffmpeg.org/legal.html).
- **Cartes OSM :** les données peuvent être utilisées avec les obligations ODbL, mais **le téléchargement massif/offline des tuiles de tile.openstreetmap.org est interdit**. Utiliser des extraits autorisés et générer/héberger ses propres données. [Politique OSM](https://operations.osmfoundation.org/policies/tiles/).
- **Musiques et paroles :** une composition, son enregistrement et ses paroles peuvent être protégés séparément, même lorsque la piste semble « gratuite ».

### 🔗 Suites dans GitHub

- [Scripts : générer le kit et vérifier l'inventaire](scripts/prepare_offline_kit.py)
- [Catalogue : 120 ressources](RESOURCES_120.csv)
- [Recettes professionnelles détaillées](KITS_PAR_METIER.md)
- [Kit de compilation APK/EXE](https://github.com/Stephen077j/Stephen077j/tree/feat/dev-build-kit-apk-exe-20261105/dev-kits/BUILD-APK-EXE) — à adapter au projet cible.

**Ce catalogue centralise les liens et les savoir-faire. Les sources restent chez leurs auteurs : aucune archive de musiques ou icônes de tiers n'est revendiquée comme appartenant au catalogue.**
