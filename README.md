# Marginal

Application web locale en français pour choisir rapidement une activité, sans compte ni API. Interface responsive, thèmes clair/sombre, filtres combinables, recommandations locales, fiches de règles, favoris et historique persistés dans `localStorage`. Le thème sombre a été retravaillé dans un style graphite plat, à contraste doux et aux angles volontairement nets, avec des adaptations tactiles spécifiques aux petits écrans.

## Lancer l’application

Ouvrez `index.html` directement dans un navigateur : le catalogue est embarqué sous forme de script local pour éviter les restrictions `fetch` des navigateurs sur `file://`. Vous pouvez aussi lancer un serveur statique local depuis ce dossier :

```bash
python3 -m http.server 8000
```

Puis ouvrez <http://localhost:8000>. Node.js n’est pas requis, aucune dépendance externe n’est utilisée et aucune connexion internet n’est nécessaire.

## Contrôler le catalogue

```bash
python3 tests/catalog-validation.py
```

Le contrôle vérifie le total exact, les identifiants, les noms/descriptions normalisés, les champs, les plages de joueurs et de durée, les règles, les matériels et les lieux. Il ne peut pas certifier qu’aucune paire ne partage une mécanique proche : cette revue sémantique reste éditoriale.

## Utilisation

1. Choisir l’effectif (1 à 999).
2. Sélectionner une ou plusieurs envies ou laisser Marginal mélanger.
3. Ajouter éventuellement des contraintes de lieu, mobilité, matériel, ambiance et durée.
4. Parcourir les idées, consulter les règles, relancer ou enregistrer un favori.

Les favoris, le thème et les dernières activités consultées/jouées restent sur l’appareil. Les outils présents dans les fiches incluent un chronomètre, le tirage d’un participant, un générateur de lettre/catégorie et un compteur de points.

## Données et limite éditoriale à connaître

`data/activities.json` contient exactement 1 000 objets statiques et validés structurellement. La première édition du catalogue est organisée comme une matrice de formats de jeu et de briefs thématiques, avec des consignes concrètes. Les contrôles automatiques repèrent les doublons textuels, mais **ne constituent pas une preuve de 1 000 mécaniques sémantiquement indépendantes**. Une revue éditoriale et des essais utilisateurs sont nécessaires avant de présenter le catalogue comme certifié « 1 000 activités distinctes » au sens strict du cahier des charges. La génération a lieu lors de la fabrication du fichier uniquement : l’application ne fabrique pas d’activités à la volée.

## Fichiers

- `index.html` : point d’entrée
- `css/style.css` : système visuel Liquid Glass, responsive et réduction des animations
- `js/app.js` : parcours, filtrage, recommandations, détails et stockage
- `data/activities.json` : catalogue embarqué
- `build_catalog.py` : construction hors ligne du JSON
- `tests/catalog-validation.py` : validation structurelle
