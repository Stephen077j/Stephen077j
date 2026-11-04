# CSV Schema Guard / Vérificateur CSV

## Français
Petit utilitaire open source **hors ligne** pour vérifier les fichiers CSV avant import dans une application (ERP, école, boutique, CRM). Il vérifie les colonnes obligatoires, les cellules vides, les identifiants en double, les en-têtes répétés et le nombre de colonnes par ligne. Le rapport JSON donne les numéros de lignes et codes d'erreurs **sans afficher les données clients**. Python 3.10+, bibliothèque standard uniquement.

```sh
cd projects/csv-schema-guard
python guard.py clients.csv --required id nom --unique id
python -m unittest discover -s . -p 'test_*.py' -v
```

Code de sortie 0 = valide ; 1 = invalide. Fichier CSV encodé UTF-8, séparateur virgule. **Limites :** ne valide pas les types de données, formats email ou règles métier. Ne modifie jamais le CSV. Les colonnes uniques conservent les valeurs en mémoire pendant la vérification : ne pas utiliser sur des fichiers géants sans adapter l'algorithme.

## English
Offline, dependency-free CSV validator for safe imports into apps. Checks required headers and values, duplicate IDs, duplicate headers and mismatched row widths. Prints machine-readable JSON error codes and line numbers **without leaking customer field values**. Python 3.10+, standard library only.

```sh
cd projects/csv-schema-guard
python guard.py customers.csv --required id name --unique id
python -m unittest discover -s . -p 'test_*.py' -v
```

Exit 0 means valid, 1 means invalid. UTF-8 comma-separated files only. Does not check field types or business rules. Never edits input. Uniqueness tracking stores keys in memory, so plan for large datasets.

## License
MIT — see LICENSE.
