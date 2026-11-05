# 💎 Trésors techniques : moteurs existants à réutiliser

**Objectif :** comprendre en 1 seconde ce que chaque projet permet de construire. Sources publiques, pas de secrets privés. Les licences, prix et compatibilités sont à confirmer avant usage commercial.

| Mon besoin | Source | Ce que je peux réutiliser | Attention |
|---|---|---|---|
| 🧾 Imprimante thermique Android 58/80 mm | [DantSu ESC/POS](https://github.com/DantSu/ESCPOS-ThermalPrinter-Android) | Bibliothèque Bluetooth, USB, TCP, formatage des tickets | Tester imprimante, caractères et permissions; dépôt sous MIT |
| 🖨️ Exemple Android complet d'impression | [thermal_printer_android_app](https://github.com/elearning-hue/thermal_printer_android_app) | Code Kotlin de transport USB/Bluetooth, PDF et image | Adapter largeur 58 mm; licence à contrôler |
| 📱 Données locales + réplication | [RxDB](https://rxdb.info/) | Base réactive et synchronisation | Conditions des plugins et conflits |
| 📴 Base hors ligne navigateur | [Dexie](https://dexie.org/) | Couche IndexedDB | Synchronisation distante à définir |
| 🔄 SQLite synchronisé | [PowerSync](https://www.powersync.com/) | Moteur de synchronisation mobile/web | Coûts et architecture |
| 🗃️ PostgreSQL synchronisé | [Electric](https://electric-sql.com/) | Flux de données vers les clients | Écritures et autorisations |
| 🤝 Documents collaboratifs | [Automerge](https://automerge.org/) | Structures CRDT | Transport et persistance |
| 📝 Édition simultanée | [Yjs](https://yjs.dev/) | Collaboration en temps réel | Réseau et authentification |
| 🎓 Gestion scolaire complète | [OpenEduCat](https://github.com/openeducat/openeducat_erp) | Modules ERP éducatifs | Éditions et licences à étudier |
| 🧭 Liste de moteurs offline-first | [awesome-local-first](https://github.com/alexanderop/awesome-local-first) | Annuaire de bibliothèques spécialisées | Vérifier chaque dépôt |
| 📚 Comparatif offline-first | [offline-first](https://github.com/yetke/offline-first) | Autres moteurs et références | Maintenance et conditions |

## Où sont cachées les ressources intéressantes ?

1. **Dossiers examples et demo :** code directement exploitable pour tester.
2. **Onglet Used by :** applications réelles utilisant la bibliothèque.
3. **Forks récents :** adaptations de matériel ou de pays.
4. **Issues fermées :** solutions à des bugs que les tutoriels n'expliquent pas.
5. **Releases :** versions compatibles et changements importants.
6. **Collections en chinois, japonais et coréen :** rechercher 开源, オープンソース et 오픈소스.
7. **Articles scientifiques avec code :** retrouver les implémentations et datasets.

## Comment choisir pour mes applications ?

- **POS / caisse / hôtel :** ESC/POS + base locale + audit financier + tests matériels.
- **École / université :** étudier OpenEduCat, puis concevoir les modules manquants.
- **Réseau local et offline :** évaluer RxDB, Yjs ou Automerge selon les données.
- **IA embarquée :** compléter l'Atlas avec des moteurs OCR, audio et traduction.

**À ne pas oublier :** gratuit ne signifie pas réutilisation commerciale autorisée. Vérifier la licence de chaque dépôt et ses dépendances. Les moteurs de synchronisation ne remplacent pas les contrôles de paiement, de sécurité et de traçabilité.

*Sélection documentaire du 05/11/2026; pas de test d'intégration effectué ici.*
