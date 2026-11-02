#!/usr/bin/env python3
"""Scaffold up to 100 independent GitHub repositories, explicitly opt-in.

Requires GitHub CLI (gh), git, credentials with repo creation rights.
Default is dry-run. Never clones, forks or copies third-party repositories.
"""
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def read_domains():
    data=json.loads((ROOT/"domains.json").read_text(encoding="utf-8"))
    domains=data["domains"]
    assert data["count"]==len(domains)==100
    assert len({d["repository"] for d in domains})==100
    assert all(re.fullmatch(r"DevCore-[A-Za-z0-9-]+",d["repository"]) for d in domains)
    return domains

def readme(d):
    name=d["name"].replace("-"," ")
    return f"""# {d['repository']} — Guide débutant / Beginner Guide

**Domaine : {name}**

Ce dépôt est le **point de départ** des ressources du domaine {name}.
Il démarre volontairement avec des modèles et une documentation : aucune intégration ni application finie n'est présumée.

## 1. Comment débuter ?
1. Installe Git et VS Code. Pour Android installe Flutter et Android Studio ; pour web installe Node.js.
2. Télécharge ce dépôt : `git clone https://github.com/OWNER/{d['repository']}.git` (remplace OWNER).
3. Ouvre `resources/catalog.json` pour identifier les sources, leurs licences et le mode d'installation.
4. Ajoute **une vraie ressource vérifiée à la fois** et documente comment la tester.
5. Place les exemples exécutables dans `starters/`, accompagnés de tests et d'un README local.

## 2. Arborescence / Directory map
- `resources/catalog.json` : références vérifiées et droits
- `apis/` : contrats et adaptateurs API (lorsqu'ils existent)
- `datasets/` : jeux de données autorisés (lorsqu'ils existent)
- `mobile/` : exemples Flutter / Android (lorsqu'ils existent)
- `web/` : exemples React / backend (lorsqu'ils existent)
- `desktop/` : outils PC (lorsqu'ils existent)
- `starters/` : modèles exécutables (lorsqu'ils existent)
- `tests/` : vérifications (lorsqu'elles existent)

## 3. Fork ou intégrer ?
**Star** = conserver un lien ; **Fork** = copier un dépôt externe sous ton compte ;
**Clone** = télécharger ; **Installer** = ajouter une dépendance ;
**Intégrer** = adapter le code au projet client et le tester.
Un fork n'est **pas** une application Android finie.

## 4. Exemple APK
Si le dossier `mobile/` contient un vrai projet Flutter (`pubspec.yaml`) :
```bash
cd mobile/NOM_DU_PROJET
flutter doctor
flutter pub get
flutter run
flutter build apk --release
```
Ne lance pas ces commandes tant qu'aucun projet Flutter n'existe.

## 5. Licences, données et sécurité
Chaque ressource doit indiquer sa source, licence, usage commercial permis ou non,
statut de vérification et date de contrôle. Ne copie pas de textes, bases de données,
contenus religieux, médicaux ou données personnelles sans droits adaptés.
Pour les domaines police/santé, ne jamais publier de dossiers réels.

## 6. Quand livrer à un client ?
Exiger tests fonctionnels, confidentialité, permissions, sauvegardes, documentation,
conditions de licence, recette et accord client. Les données/API tierces nécessitent
souvent des comptes et autorisations.

## English
Start with the resources catalog. Verify each upstream license before reusing code
or data. Install the appropriate toolchain and only run the commands for projects
that actually exist. Test the adapted client application before deployment.
"""

def setup_files(folder,d):
    folder.mkdir(parents=True,exist_ok=True)
    (folder/"README.md").write_text(readme(d),encoding="utf-8")
    (folder/".gitignore").write_text(".env\n.env.*\n!.env.example\nnode_modules/\n.venv/\n*.db\n",encoding="utf-8")
    (folder/"resources").mkdir(exist_ok=True)
    data={"domain":d["name"],"sources":[],"instructions":"Add verified GitHub project URLs, documentation, license and last review date. Do not claim a fork until performed."}
    (folder/"resources"/"catalog.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (folder/"START-HERE.md").write_text("Commence par README.md et resources/catalog.json. Aucun code tiers n'est copié.\n",encoding="utf-8")

def command(args,folder):
    subprocess.run(args,cwd=folder,check=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--limit",type=int,default=5,help="Maximum repositories to plan/create (1..100)")
    p.add_argument("--execute",action="store_true",help="Explicitly create GitHub repositories")
    p.add_argument("--public",action="store_true",help="Use public repositories (default: private)")
    p.add_argument("--only",help="Exact domain repository name, e.g. DevCore-Bible-Hymns")
    args=p.parse_args()
    if not 1<=args.limit<=100:p.error("--limit must be between 1 and 100")
    entries=read_domains()
    if args.only:
        entries=[d for d in entries if d["repository"]==args.only]
        if not entries:p.error("unknown repository name")
    selected=entries[:args.limit]
    print(("EXECUTION" if args.execute else "DRY RUN")+f": {len(selected)} repositories")
    for d in selected:print(" -",d["repository"],"public" if args.public else "private")
    if not args.execute:
        print("Nothing created. Add --execute to explicitly create using gh CLI.")
        return
    if shutil.which("gh") is None or shutil.which("git") is None:
        raise SystemExit("Install Git and GitHub CLI (gh) first.")
    command(["gh","auth","status"],Path.cwd())
    with tempfile.TemporaryDirectory() as temporary:
        for d in selected:
            folder=Path(temporary)/d["repository"]
            setup_files(folder,d)
            command(["git","init","-b","main"],folder)
            command(["git","add","."],folder)
            command(["git","-c","user.name=DevCore Repository Factory","-c","user.email=devcore-factory@users.noreply.github.com","commit","-m","docs: initial beginner domain guide"],folder)
            # CLI will fail on existing repos: they are never overwritten.
            command(["gh","repo","create",d["repository"],"--public" if args.public else "--private","--source=.","--remote=origin","--push"],folder)
            print("Created:",d["repository"])
if __name__=="__main__":
    main()
