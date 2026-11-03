# Sentiment Lite — FR / EN / MG

## Français
Petit outil **hors ligne** pour classer des commentaires clients CSV en `positive`, `negative` ou `neutral`. Python 3.10+ ; **aucune dépendance externe**. Prise en charge de mots fréquents en français, anglais et malgache. Les négations simples (`pas`, `not`, `tsy`) inversent le score des deux mots suivants.

```sh
cd projects/sentiment-lite
python sentiment.py input.csv output.csv --column comment
python -m unittest discover -s . -p 'test_*.py' -v
```

CSV d'entrée : `id,comment` ; sortie : colonnes d'origine + `sentiment,score`. Ne jamais utiliser pour des décisions sensibles : lexique réduit, pas d'apprentissage automatique, ironie et variations linguistiques non maîtrisées. Ne pas envoyer de données personnelles sans consentement.

## English
Small **offline** CSV customer-comment classifier with positive/negative/neutral labels and a transparent lexicon score. Python 3.10+, standard library only. Includes basic French, English and Malagasy words and nearby negation handling. Run the same commands above; input must contain a `comment` column by default. This is a baseline, **not a validated production sentiment model**. Expand and evaluate the lexicon on representative labeled data before deployment.

## License
MIT — see LICENSE. Contributions should include tests and no real customer data.
