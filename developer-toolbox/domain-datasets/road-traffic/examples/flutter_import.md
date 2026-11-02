# Charger un fichier JSON dans une APK Flutter

1. Crée une vraie application Flutter : `flutter create code_route_app`
2. Dans ton application, crée `assets/data/` et copie le JSON d'un pays sous le nom `road_signs.json`.
3. Ajoute dans `pubspec.yaml` (attention à l'indentation) :

```yaml
flutter:
  assets:
    - assets/data/road_signs.json
```

4. Dans une page Dart :

```dart
import 'dart:convert';
import 'package:flutter/services.dart';

Future<List<Map<String, dynamic>>> readRoadData() async {
  final jsonString = await rootBundle.loadString('assets/data/road_signs.json');
  final decoded = jsonDecode(jsonString) as Map<String, dynamic>;
  return (decoded['entries'] as List<dynamic>)
      .map((item) => Map<String, dynamic>.from(item as Map))
      .toList();
}
```

5. Appelle `readRoadData()` et affiche `name` et `description` dans une liste. Teste le mode avion.
6. Avant une livraison, vérifie la validité locale des données et les droits des illustrations. Ce fragment est un exemple d'import, pas une APK déjà construite.
