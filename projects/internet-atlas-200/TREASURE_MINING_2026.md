# 💎 Treasure Mining 2026 — moteur de découverte mondial

**Mission :** trouver les briques techniques déjà publiées, pas seulement les sites populaires. **Statut : prototype de collecte reproductible; aucune exploration massive n'a encore été exécutée.**

## ⚡ Trouver la bonne ressource en une seconde

| Besoin | Moteur / source | Ce qu'on récupère | Limite |
|---|---|---|---|
| 🧭 Millions de dépôts et dépendances | [ecosyste.ms](https://ecosyste.ms/) | Métadonnées, licences, relations | Les licences commerciales des données peuvent différer |
| 🗂️ Collections thématiques cachées | [Awesome ecosyste.ms](https://awesome.ecosyste.ms/) | Listes spécialisées, projets associés | Chaque lien doit être revérifié |
| 📦 Bibliothèques réutilisables | [Packages ecosyste.ms](https://packages.ecosyste.ms/) | Paquets, versions, registres | Pas nécessairement des applications |
| 🗣️ Reconnaissance vocale | [FunASR](https://github.com/modelscope/FunASR) | Moteur ASR, VAD, diarisation | Langues, matériel et licence des modèles |
| 🎬 Génération vidéo / image | [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio) | Outils de modèles de diffusion | Calcul et licences des poids |
| 🧠 Évaluation des IA | [EvalScope](https://github.com/modelscope/evalscope) | Mesures et bancs d'essai | Configurer jeux de test |
| 📖 Livres informatiques chinois | [awesome-cs-books](https://github.com/imarvinle/awesome-cs-books) | Index de livres et connaissances | Vérifier droits de chaque document |
| 🐍 Bibliothèques Python en chinois | [awesome-python-cn](https://github.com/jobbole/awesome-python-cn) | Listes par besoin | Vérifier actualité des dépôts |
| 🧩 Applications Python complètes | [awesome-python-applications](https://github.com/mahmoud/awesome-python-applications) | Exemples d'applications réelles | Évaluer chaque application |
| 📚 Construire des moteurs | [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | Guides pour créer systèmes et moteurs | Principalement apprentissage |
| 🔧 Déploiement autonome | [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) | Logiciels installables | Vérifier sécurité et maintenance |
| 📱 Bibliothèques Flutter | [awesome-flutter](https://github.com/Solido/awesome-flutter) | Composants mobiles | Tester compatibilité Flutter |

## 🎯 Ce qu'on collecte pour chaque trouvaille

**Besoin utilisateur → Nom → Lien source → Type (application/moteur/dataset/guide) → Fonction réelle → Démo → Licence → Usage commercial → Langue → Dernière activité → État de vérification → Priorité.**

**Important :** « URL répertoriée » n'est pas « testée », « open source » n'est pas « réutilisable sans conditions » et « indexé » n'est pas « validé ». Ne pas inventer de score de sécurité ou de licence.

## 🔎 Pistes de fouille mondiale

- Chine : GitHub, ModelScope, collections en chinois; chercher `开源`, `源码`, `完整项目`.
- Japon : chercher `オープンソース`, `業務システム`.
- Corée : chercher `오픈소스`, `프로젝트`.
- Inde, Indonésie, Vietnam : recherches anglaises et langues locales.
- Sciences : logiciels cités dans les articles, codes de reproduction, jeux de données.
- Industrie : logiciels POS, impression, ERP, énergie, cartographie, santé, agriculture.
- GitHub : fichiers examples, forks maintenus, releases, dépendants et problèmes résolus.

## 🤖 Collecte automatisée (prototype)

Exécuter localement : `python3 scripts/discover_github.py --output discoveries.csv`

Le script recherche via **l'API officielle GitHub**, non par contournement des protections. Il limite le nombre de requêtes, respecte les réponses 403/429, et produit un CSV de candidats **non audités**. Aucun code tiers n'est téléchargé ni copié.

## ⚖️ Limites

Les catalogues publics peuvent contenir des projets obsolètes, frauduleux ou sous licence incompatible. Ne jamais exécuter automatiquement le code découvert, aspirer des données privées, contourner des limitations d'accès, ni publier des données sans autorisation. Pour les systèmes financiers, prévoir tests, permissions et traçabilité.
