# DevCore — 100 Domain Repository Factory

**Goal / Objectif :** transform the 100-domain roadmap into **100 independent GitHub repositories**, each with a beginner-friendly bilingual README, resource catalog and setup instructions.

## What is actually available now?
- [domains.json](domains.json) defines **100 distinct repository names**.
- [create_repos.py](create_repos.py) is a **dry-run by default** GitHub CLI factory.
- Templates include beginner guidance for Git, Flutter, sources, licences and APK build prerequisites.
- **No 100 repositories have yet been created by this change.** The connected GitHub integration cannot create repositories. You can run the factory using GitHub CLI with your own authenticated account.

## Windows beginner tutorial

1. Install **Git**, **Python 3.11+** and **GitHub CLI** from their official sources.
2. Open PowerShell and authenticate:
   ```powershell
   gh auth login
   gh auth status
   ```
3. Download/clone your existing repository:
   ```powershell
   git clone https://github.com/Stephen077j/Stephen077j.git
   cd Stephen077j/developer-toolbox/domain-factory
   ```
4. Preview first five repos (**creates nothing**):
   ```powershell
   python create_repos.py --limit 5
   ```
5. Create **one private repository** to validate your permissions:
   ```powershell
   python create_repos.py --only DevCore-Bible-Hymns --execute
   ```
6. Create the remaining repositories when ready:
   ```powershell
   python create_repos.py --limit 100 --execute
   ```
   Already-existing repositories are not overwritten; GitHub CLI returns an error for a duplicate. This is intentional. You can create subsets with `--limit` or choose `--only`.
7. Public only when intended: append `--public`. **Default is private**.

## Important notes

- Each newly created repo contains **initial documentation and an empty resources catalog**, **not copied third-party software**. Fill them with verified upstream URLs and tested examples over time.
- Never place access tokens in a file or commit. The script uses `gh auth`.
- Creating 100 repositories at once can trigger GitHub limits. Start with one, then small batches.
- Repository creation may require permission review on your account or organization.
- For actual working code and example API modules, see [DevCore business starter](../freelance/business-starter/) and [sector catalog](../sector-kits/).
