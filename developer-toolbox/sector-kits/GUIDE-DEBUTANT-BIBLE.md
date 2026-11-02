# Exemple débutant — Créer une application Bible et cantiques

## Ce que tu veux faire
Une application Android avec Bible, numéros de cantiques, recherche et favoris, utilisable hors ligne.

## 1. Où chercher dans ta bibliothèque ?
- Ton code existant : [ezra-fihirana](https://github.com/Stephen077j/ezra-fihirana).
- Ressources bibliques : [Bible Data](https://github.com/midvash/bible-data).
- Annuaire par domaine : [Sector Kits](README.md).

**Ne suppose pas que les textes et paroles sont libres de droits.** Vérifie les droits de chaque traduction et recueil adventiste. Ne publie pas une copie protégée sans autorisation.

## 2. Quel code faut-il pour l'APK ?
- **Flutter** : les écrans du lecteur et la navigation.
- **SQLite/JSON** : les livres, versets et titres/numéros de cantiques autorisés.
- **Stockage local** : favoris et historique de lecture.
- **Tests** : recherche, liens verset, changement de langue et fonctionnement hors ligne.

## 3. Étapes concrètes
1. Installer Git, Flutter et Android Studio.
2. Ouvrir un terminal et exécuter `flutter doctor`.
3. Cloner ton dépôt de base si son contenu est adapté : `git clone https://github.com/Stephen077j/ezra-fihirana.git`.
4. Examiner le README et les fichiers du dépôt pour identifier le langage/framework réellement utilisé.
5. Si ce n'est pas une application Flutter, ne lance pas immédiatement `flutter run` : crée un projet Flutter distinct (`flutter create lecteur_bible`) puis adapte les éléments compatibles.
6. Ajouter uniquement les données bibliques et cantiques que tu as le droit de distribuer.
7. Tester sur téléphone : chercher un verset, ouvrir un cantique, enregistrer un favori, couper Internet.
8. Dans un projet Flutter prêt, exécuter `flutter build apk --release` puis vérifier la signature et l'installation.

## 4. Ce qui reste à créer
Le dépôt sectoriel fournit **un guide et des sources**, pas encore une APK Bible finale vérifiée. L'intégration Flutter et les données légales doivent encore être testées.

## Autres métiers
La même méthode s'applique à l'école, la santé, le commerce, la sécurité publique et l'agriculture : identifier le projet, vérifier les licences, récupérer le code autorisé, personnaliser, tester et livrer.
