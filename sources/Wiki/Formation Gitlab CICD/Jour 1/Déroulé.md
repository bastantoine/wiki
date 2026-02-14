- Partie 1 & 2
- Partie 3.1 : Runners
- Exercice :
1. Mettre en place une chaine de CI qui lance tous les tests à chaque fois
2. Rajouter un job pour le lint du code avec flake8

- Partie 3.2 : Variables
- Partie 3.3 : Règles d'exécution conditionnelle
- Partie 3.4 : Evénement déclenchant une pipeline
- Exercice :

3. Travail sur les conditions de lancement des jobs :
	- Lancer les tests et le lint que lorsque la pipeline est lancée dans une branche qui a au moins une merge request d'ouverte
	- Rendre le lint du code non bloquant
4. Ajouter un job qui fait le build & push docker
   - no push si sur une branche != main avec une MR ouverte
   - push uniquement si sur la branche par défaut
5. Ajouter 3 stages de déploiement en dev, rct & prd
   - uniquement si commit sur les branches deploy/dev, deploy/rct et deploy/prd
     - ne pas ajouter le job sinon
   - deploy prd en manual seulement
   - besoin de variables sécurisées pour le déploiement
   - autoriser le push docker sur ces branches la

- Partie 3.5 : Artefacts

6. Ajouter un stage qui réalise le lint du swagger
	- nécessite un stage au préalable qui génère le swagger
	- le job de lint ne doit pas être bloquant
7. Générer les rapports JUnit pour les tests unitaires et le swagger, et le rapport de couverture