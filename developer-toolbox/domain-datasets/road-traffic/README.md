# DevCore Road Traffic Data — données internationales pour APK

**Premier domaine réellement commencé** : code de la route / signalisation. Structure régionale avec JSON téléchargeables. Les données actuelles contiennent **8 fiches de départ dans 5 pays** (États-Unis, Royaume-Uni, France, Japon, Madagascar), pas tous les panneaux ni toutes les lois.

## Pour débuter
1. Clique sur `datasets/` et choisis un pays : `anglophone/us`, `anglophone/uk`, `francophone/france`, `asia/japan`, `madagascar`.
2. Ouvre `entries.json` puis clique **Raw** ou **Download raw file** pour sauvegarder le JSON.
3. Copie le fichier dans `assets/data/` de ton application Flutter et référence le dossier dans `pubspec.yaml`.
4. Lis `examples/flutter_import.md` pour charger ces données dans l'application.
5. Vérifie le pays, la licence des images, la mise à jour des règles et la qualité avant publication.

## Structure
```text
datasets/
  anglophone/us/entries.json
  anglophone/uk/entries.json
  francophone/france/entries.json
  asia/japan/entries.json
  madagascar/entries.json
sources.json
scripts/validate.py
examples/flutter_import.md
```

Les dossiers sont géographiques ; la langue de chaque JSON est indiquée dans `language`. Les fiches Japon et Madagascar sont des **pointeurs juridiques**, pas des cours complets. Aucun visuel soumis à licence tierce n'a été copié.

## English
Download `entries.json` from the country folder, import it into Flutter assets and parse JSON locally. **This is a small curated starter pack, not an authoritative driving-test database.** Review current national rules, licenses and source dates before commercial reuse.

## Prochaines collectes nécessaires
Panneaux supplémentaires, règles propres à chaque pays, visuels libres de droits, QCM vérifiés, traductions locales et historique des modifications. Ne pas inventer des limitations de vitesse ni mélanger les pays.
