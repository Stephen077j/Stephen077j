# DevCore Sector Kits — Réserve de projets par métier

**But :** quand un client te demande une APK, un site ou un logiciel métier, commence par ce catalogue plutôt que rechercher les mêmes dépôts.

## Scénario concret : Bible + cantiques adventistes

1. Trouver un moteur de lecture et des données bibliques dans [Bible Data](https://github.com/midvash/bible-data) ou [Awesome Bible Developer Resources](https://github.com/biblenerd/awesome-bible-developer-resources).
2. Vérifier ton dépôt [ezra-fihirana](https://github.com/Stephen077j/ezra-fihirana), puis identifier les fonctionnalités réutilisables : recherche, favoris, hors ligne, navigation par numéro, typographie.
3. **Attention :** les paroles de cantiques adventistes et certaines traductions malgaches de la Bible peuvent être protégées. Demander des droits ou une source libre explicite ; une APK publique ne donne pas le droit de recopier ses contenus.
4. Créer une nouvelle application Flutter indépendante, importer uniquement les contenus autorisés et tester Android hors ligne.

## Autres exemples

| Client | Première ressource | Ce qu'il faut développer/personnaliser |
|---|---|---|
| École sans Internet | [Kolibri](https://github.com/learningequality/kolibri) | Programmes, contenu autorisé, accès parents, synchronisation |
| Université | [Moodle](https://github.com/moodle/moodle) + [university-reference](https://github.com/Stephen077j/university-reference) | Inscriptions, notes, règlements, diplômes |
| Police / service public | [PIRMS](https://github.com/shizzleclover/PIRMS), [PIMS](https://github.com/shreya-25/PIMS) | Données de test seulement ; rôles, audits, chiffrement, législation |
| Exploitation agricole | [farmOS](https://github.com/farmOS/farmOS) | Cultures, parcelles, stocks, activités, géolocalisation |
| Cabinet médical | [OpenMRS](https://github.com/openmrs/openmrs-core) | Confidentialité, consentement, données médicales |
| Commerce | [ERPNext](https://github.com/frappe/erpnext) / [Medusa](https://github.com/medusajs/medusa) | Produits, caisse, paiements, taxes |
| Hôtel | [QloApps](https://github.com/Qloapps/QloApps) | Réservations, chambres, encaissement |
| Transport | [OpenTripPlanner](https://github.com/opentripplanner/OpenTripPlanner) | Cartes autorisées, horaires réels |

## Fork n'est pas intégration

- **Star :** garder le dépôt en favori.
- **Fork :** créer une copie du code dans ton compte, si GitHub te l'autorise.
- **Clone :** récupérer le code localement.
- **Intégration :** adapter les modules, dépendances, base de données, licences et tests à la nouvelle application.
- **Build APK :** compiler le projet Android, après les tests.

**Le catalogue [catalog.json](catalog.json) identifie explicitement les références externes et les dépôts déjà présents sur ton compte. Il n'affirme pas que des forks ont été réalisés.** L'accès à un dépôt ne prouve pas que son contenu est librement redistribuable.

## Vérification avant mission client

- Licence du **code** et licence des **données** vérifiées séparément.
- État du dépôt, dernières mises à jour, vulnérabilités et dépendances.
- Fonctionnement local testé ; aucune donnée privée copiée.
- Configuration du pays, langues, mode hors ligne et appareils.
- Cahier des charges, prix, livraison, maintenance, consentements et conformité.

Les secteurs police et santé exigent des contrôles plus stricts, notamment la protection des personnes, la traçabilité et l'accès limité aux données.


## Débuter sans expérience / Beginner setup

- **[Modèle de README pour chaque futur dépôt par métier](BEGINNER-README-TEMPLATE.md)** : installation, Flutter, Python, React, intégration, APK, dépannage.
- **[Exemple guidé : application Bible et cantiques](GUIDE-DEBUTANT-BIBLE.md)** : quelles ressources récupérer, les droits et comment débuter une APK.

Les guides indiquent clairement la différence entre ressources référencées, code réellement présent et applications entièrement testées.
