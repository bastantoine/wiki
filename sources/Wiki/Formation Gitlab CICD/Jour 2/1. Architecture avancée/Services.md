---
title: "Services"
tags:
- GitlabCI
---
Les services sont des conteneurs lancés en parallèle d'un job et auxquels le job a accès. Ils peuvent être utilisés, par exemple, pour mettre à disposition une base de donnée à des jeux de tests.

> [!warning]
> Ce mécanisme ne peut être utilisé que pour des services accessibles via le réseau. Tout autre moyen d'interaction avec le service additionnel n'est pas possible. Le job suivant ne fonctionne pas :
> ```yaml
> job:
>   services:
>     - php:7
>     - node:latest
>     - golang:1.10
>   image: alpine:3.7
>   script:
>     - php -v
>     - node -v
>     - go version
> ```

## Exemple
L'exemple suivant lance un conteneur avec une base MySQL en parallèle du job. Le job lui execute un script python qui se connecte à la base et effectue quelques opérations.

```yaml
stages:
  - test

test:
  stage: test
  image: python:3.11
  variables:
    MYSQL_USER: user
    MYSQL_PASSWORD: password
    MYSQL_DATABASE: database
  script:
    - export MYSQL_HOST=mysql
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install --upgrade pip
    - pip install -r requirements.txt
    - python script.py
  services:
    - name: mysql:latest
      variables:
        MYSQL_ROOT_PASSWORD: password
```

```python
from sqlalchemy import create_engine, text
import os

if __name__ == '__main__':
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    conn_query = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    engine = create_engine(conn_query)
    engine.connect()

    with engine.connect() as conn:
        # Prepare the DB and data
        conn.execute(text("""CREATE TABLE client
(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    prenom VARCHAR(100),
    nom VARCHAR(100),
    ville VARCHAR(255),
    age INT
)"""))
        conn.execute(text("""INSERT INTO client (prenom, nom, ville, age)
 VALUES
 ('Rébecca', 'Armand', 'Saint-Didier-des-Bois', 24),
 ('Aimée', 'Hebert', 'Marigny-le-Châtel', 36),
 ('Marielle', 'Ribeiro', 'Maillères', 27),
 ('Hilaire', 'Savary', 'Conie-Molitard', 58)"""))

        # Search for any data
        result = conn.execute(text("""SELECT * FROM client"""))
    for row in result.fetchall():
        print(row._asdict())
```

## Configuration
Comme tout conteneur Docker, la configuration des services se fait via des variables d'environnement.

Toutes les variables accessibles par le job seront automatiquement mises à disposition des services créés.

> [!warning]
> Attention aux potentiels conflits dans les noms des variables définies en dehors.

Les services ont accès au fichiers du job puisque le dossier du job est monté en tant que volume au path `/build`.

## Accès au service depuis le job
Lors du lancement des conteneurs pour le job et le(s) service(s) configurés, l'executor du runner va créer un lien entre les différents conteneurs afin qu'il soient tous accessibles les uns des autres.

Lorsque les services sont lancés, chacun est accessible via deux hostnames déterminés automatiquement à partir de l'image utilisée :
1. Tout ce qu'il y a après les `:` est supprimé
2. Chaque slash `/` est remplacé par des doubles underscores `__` afin de former l'alias principal
2. Chaque slash `/` est remplacé par un tiret simple `-` afin de former l'alias secondaire.

![[Formation Gitlab CICD/Jour 2/Attachements/Service name aliases.svg]]

> [!note]
> Chaque service dispose de deux alias avec lesquels il est joignable. L'alias secondaire est nécessaire puisque les hostname contenant des underscores ne sont pas valides, et ainsi peuvent causer des comportements imprévus selon les systèmes.

> [!note]
> Il est possible de fournir un autre alias au service, via le keyword `[job].services.alias`. Ainsi le service en question sera joignable via cet alias, et uniquement celui ci.

## Disponibilité de la fonctionnalité
Puisque le mécanisme de services se base sur des conteneurs Docker, il ne peut nécessaire que fonctionner sur des runners avec des executors Docker ou Kubernetes.