# QuoteFlow — Vite + PHP

Open-source quotation builder with a responsive Vite frontend and an independent PHP validation API. **Prototype, not a production billing system.**

## Requirements
Node.js 20+, npm and PHP 8.1+.

## Run
```bash
npm install
php -S 127.0.0.1:8000 -t .
# In another terminal:
npm run dev
```
Vite proxies /api to the PHP server. `npm test` runs calculation tests; `php -l api/quote.php` checks PHP syntax.

## Features
Quote items, tax calculations, JSON export, and PHP validation endpoint. Amounts are illustrative and not legally compliant invoices.

## Français
Création de devis, taxes, export JSON et validation des montants via API PHP. Démonstration uniquement : aucune authentification, aucun paiement, aucune conservation des données.
