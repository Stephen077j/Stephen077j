# File Integrity Lite — Offline SHA-256 inventory

## Français

Petit outil Python 3.10+ **sans dépendance externe** pour créer un inventaire JSON des fichiers d'un dossier et vérifier ensuite leur intégrité. Utile pour contrôler des sauvegardes, dossiers de livraison et exports de projets. Chaque entrée contient un chemin relatif, une taille et un SHA-256 ; aucun contenu de fichier n'est stocké. Les liens symboliques sont ignorés pendant l'inventaire. Les chemins traversant hors du dossier sont refusés pendant la vérification.

```sh
cd projects/file-integrity-lite
python integrity.py create ./mon-dossier inventaire.json
python integrity.py verify ./mon-dossier inventaire.json
python -m unittest discover -s . -p 'test_*.py' -v
```

Le manifeste doit être enregistré **hors du dossier inventorié** si possible. `create` refuse d'écraser un manifeste existant. Code de sortie : 0 = vérification OK, 1 = fichiers modifiés/manquants, 2 = erreur de lecture ou format. **Limites :** les nouveaux fichiers non listés ne sont pas détectés ; SHA-256 vérifie l'intégrité, pas l'authenticité d'un manifeste non signé. Protéger le manifeste contre les modifications non autorisées.

## English

Python 3.10+ **dependency-free**, offline SHA-256 file inventory and verification tool. Create a JSON manifest with relative paths, file sizes and checksums; verify a directory later. Useful for backup checks, software deliverables and export verification. File contents are never stored. Symlinks are skipped during inventory; unsafe traversal paths are rejected during verification.

```sh
cd projects/file-integrity-lite
python integrity.py create ./my-folder manifest.json
python integrity.py verify ./my-folder manifest.json
python -m unittest discover -s . -p 'test_*.py' -v
```

Prefer placing the manifest **outside the inventoried folder**. Creation never overwrites an existing manifest. Exit codes: 0 = OK, 1 = mismatch, 2 = input/format error. **Limitations:** new files absent from the manifest are not flagged. SHA-256 detects changes but does not authenticate an unsigned manifest; store manifests securely.

## License

MIT — see LICENSE.
