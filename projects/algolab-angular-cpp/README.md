# AlgoLab — Angular + C++17

An Angular statistical dashboard with a **separate native C++17 command-line implementation** of the same calculations. Demonstrates frontend engineering, numeric validation, native compilation and parity testing. Angular does **not** run C++ in the browser.

## Angular
Node.js 20+ and npm:
```bash
npm install
npm start
```
Open the local Angular address (normally http://localhost:4200).

## C++ CLI
```bash
g++ -std=c++17 -Wall -Wextra -pedantic cpp/analyze.cpp -o analyze
./analyze cpp/sample.csv
```

## Tests
`npm run test:ts` invokes a Node-based C++ compilation test (g++ required). `npm run build` checks the Angular build after dependency installation.

## Limitations
At most 1000 numeric values; no CSV headers or advanced quoted CSV parsing. The two implementations are independent, and data remains local.

## Français
Application Angular de statistiques (effectif, minimum, maximum, moyenne, médiane) avec un programme C++ indépendant produisant les mêmes calculs sur un fichier CSV.
