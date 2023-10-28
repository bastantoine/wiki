---
title: "Architecture avancée"
tags:
- GitlabCI
---
## Paramètres globaux
Certains paramètres des jobs peuvent être définis au niveau global de la pipeline. Leur définition affecte l'ensemble des jobs de la pipeline.

Les paramètres définis au niveau global peuvent être redéfinis au niveau de chaque job, auquel cas la valeur définie dans le job aura précédence. Il est possible de contrôler quels paramètres sont hérités, voire désactiver complètement l'héritage des paramètres globaux pour un job donné avec, `[job].inherit.default` et `[job].inherit.variables` [\[ref\]](https://docs.gitlab.com/ee/ci/jobs/index.html#control-the-inheritance-of-default-keywords-and-global-variables).

```yaml
default:
  retry: 2
  image: ruby:3.0
  interruptible: true

job1:
  script: echo "This job does not inherit any default keywords."
  inherit:
    default: false

job2:
script: echo "This job inherits only the two listed default keywords. It does not inherit 'interruptible'."
  inherit:
     default:
      - retry
      - image
```

Les paramètres pouvant être définis au niveau global sont :
- [`artifacts`](https://docs.gitlab.com/ee/ci/yaml/#artifacts)
- [`after_script`](https://docs.gitlab.com/ee/ci/yaml/#after_script)
- [`before_script`](https://docs.gitlab.com/ee/ci/yaml/#before_script)
- [`cache`](https://docs.gitlab.com/ee/ci/yaml/#cache)
- [`hooks`](https://docs.gitlab.com/ee/ci/yaml/#hooks)
- [`image`](https://docs.gitlab.com/ee/ci/yaml/#image)
- [`interruptible`](https://docs.gitlab.com/ee/ci/yaml/#interruptible)
- [`retry`](https://docs.gitlab.com/ee/ci/yaml/#retry)
- [`services`](https://docs.gitlab.com/ee/ci/yaml/#services)
- [`tags`](https://docs.gitlab.com/ee/ci/yaml/#tags)
- [`timeout`](https://docs.gitlab.com/ee/ci/yaml/#timeout)

[\[ref\]](https://docs.gitlab.com/ee/ci/yaml/#default)

## Héritage de jobs
Plusieurs manières sont possibles pour faire en sorte qu'un job hérite d'un autre :
1. À l'aide des [[Formation Gitlab CICD/Jour 2/1. Architecture avancée/Factorisation de la config#Références YAML | références YAML]]
2. À l'aide du [[Formation Gitlab CICD/Jour 2/1. Architecture avancée/Factorisation de la config#Utilisation du keyword `extends` | keyword `extends`]]
3. À l'aide du [[Formation Gitlab CICD/Jour 2/1. Architecture avancée/Factorisation de la config#Utilisation du tag `!reference` | tag `!reference`]]
4. À l'aide d'[[Formation Gitlab CICD/Jour 2/1. Architecture avancée/Factorisation de la config#Inclusions externes | inclusions externes]]

### Références YAML
Le langage YAML propose une fonctionnalité de références, permettant de faire référence à certaines portions d'un fichier YAML au sein du même fichier, afin de les réutiliser à différents endroits.

En utilisant les jobs cachés (ie. des jobs dont le nom commence par un point), on peut définir des templates réutilisables à différents endroits du fichier de config. La syntaxe est la suivante :

- `&< key >`: permet d'associer une clé `key` à un mapping clé-valeur ou une liste
- `*< key >`: insert la configuration identifiée par la clé `key` comme valeur d'une clé donnée dans le cas d'un mapping, ou comme élément d'une liste dans le cas d'une liste
- `<<: *< key >`: insert la configuration identifiée par la clé `key` au sein du mapping clé-valeur actuel

```yaml
.job_template: &job_configuration
  script:
    - test project
  tags:
    - dev

.postgres_services:
  services: &postgres_configuration
    - postgres
    - ruby

.mysql_services:
  services: &mysql_configuration
    - mysql
    - ruby

test:postgres:
  <<: *job_configuration
  services: *postgres_configuration
  tags:
    - postgres

test:mysql:
  <<: *job_configuration
  services: *mysql_configuration
```

Une fois les remplacements effectués, ce fichier serait équivalent à :

```yaml
.job_template:
  script:
    - test project
  tags:
    - dev

.postgres_services:
  services:
    - postgres
    - ruby

.mysql_services:
  services:
    - mysql
    - ruby

test:postgres:
  script:
    - test project
  services:
    - postgres
    - ruby
  tags:
    - postgres

test:mysql:
  script:
    - test project
  services:
    - mysql
    - ruby
  tags:
    - dev
```

Lors de l'utilisation de références YAML, il est possible de redéfinir une valeur héritée d'une référence. Il suffit pour cela de fournir une nouvelle valeur.

> [!warning]
> Si un paramètre est défini au sein d'une référence, ainsi que là où la référence est utilisée, c'est la dernière valeur qui est pris en compte.
>
> Ainsi pour que la surcharge du paramètre soit correctement effectuée, il faut qu'il soit redéfini après l'utilisation de la référence YAML.
>
> Avec la config suivante, une fois les références résolues, le `job-1` aura comme image `python:3.11` alors que le `job-2` utilisera `python:3.10` :
> ```yaml
> .default-python-image: &default-python-image
>   image: python:3.10
>
> job-1:
>   <<: *default-python-image
>   image: python3.11
>
> job-2:
>   image: python3.11
>   <<: *default-python-image
> ```

### Utilisation du keyword `extends`
Gitlab propose le keyword [`extends`](https://docs.gitlab.com/ee/ci/yaml/index.html#extends) afin de permettre la réutilisation de différentes portion de config. Son utilisation est similaires aux ancres YAML, mais plus simple et plus flexible dans son usage.

Exemple :

```yaml
.tests:
  script: rake test
  stage: test
  only:
    refs:
      - branches

rspec:
  extends: .tests
  script: rake rspec
  only:
    variables:
      - $RSPEC
```

Une fois mergé, le fichier de config serait le suivant :
```yaml
rspec:
  script: rake rspec
  stage: test
  only:
    refs:
      - branches
    variables:
      - $RSPEC
```

Il est possible d'étendre plusieurs configurations à la fois :
```yaml
.only-important:
  tags:
    - production
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

.in-docker:
  tags:
    - docker
  image: alpine

build:
  extends:
    - .only-important
    - .in-docker
  script: echo
```

> [!info]
> Dans le cas où des paramètres hérités de configurations référencées via `extends` sont redéfinis au niveau du job, c'est toujours la valeur du job qui sera prise en compte, et ce quelque soit l'ordre dans lequel la déclaration du `extends` et la redéfinition du paramètre sont faits.
>
> Ainsi dans la configuration suivante, les deux jobs `job-1`et `job-2` auront tout deux `python:3.11` comme image :
> ```yaml
> .default-python-image:
>   image: python:3.10
>
> job-1:
>   extends: .default-python-image
>   image: python3.11
>
> job-2:
>   image: python3.11
>   extends: .default-python-image
> ```
>
> Cependant, dans le cas où un job hérite de plusieurs configurations via `extends`, si un paramètre est défini dans plusieurs configurations à la fois, seule la dernière définition sera prise en compte (ie. la configuration la plus proche de la fin de la liste des héritages).

> [!info]
> `extends`supporte jusqu'à 11 niveaux d'héritage, mais il est recommandé de se limiter à 2 ou 3 niveaux, au delà la complexité supplémentaires apportée rends les configurations difficiles à manipuler.

### Utilisation du tag `!reference`
Gitlab propose le tag YAML custom `!reference` permettant de réutiliser des portions de configuration dans la définition des jobs. Cette syntaxe est similaire aux références YAML, mais est plus flexible.

```yaml
.vars:
  variables:
    URL: "http://my-url.internal"
    IMPORTANT_VAR: "the details"

test-vars-1:
  variables: !reference [.vars, variables]
  script:
    - printenv

test-vars-2:
  variables:
    MY_VAR: !reference [.vars, variables, IMPORTANT_VAR]
  script:
    - printenv
```
[\[ref\]](https://docs.gitlab.com/ee/ci/yaml/yaml_optimization.html#reference-tags)

### Inclusions externes
Avec les références YAML, `extends` et `!reference`, il est possible de réutiliser des configurations au sein d'un même fichier.

Le keyword [`include`](https://docs.gitlab.com/ee/ci/yaml/index.html#include) permet d'inclure des fichiers externes au sein d'un fichier de configuration.

```yaml
include: '/templates/cicd-template.yml'
```

Plusieurs types d'inclusions sont possibles :
- `include:local` : inclure un fichier présent dans le projet courant [\[ref\]](https://docs.gitlab.com/ee/ci/yaml/index.html#includelocal)
- `include:remote` : inclure un fichier accessible via une URL HTTP ou HTTPS [\[ref\]](https://docs.gitlab.com/ee/ci/yaml/index.html#includeremote)
- `include:project` : inclure un fichier présent dans un autre projet [\[ref\]](https://docs.gitlab.com/ee/ci/yaml/index.html#includeproject)

> [!note] Notes
> - Les fichiers accessibles via une URL pour les inclusions remote doivent être accessible par une requête GET sans authentification.
> - Lorsqu'un fichier référencé via un `include:project` est privé, l'utilisateur qui lance la pipeline doit être membre des deux projets pour que l'inclusion puisse se faire.
> - Si le type d'inclusion n'est pas indiqué, les liens commençant par `http://` ou `https://` seront considérés comme des remote, tandis que les autres seront considérés comme des inclusions de fichiers locaux.

Il est possible d'inclure plusieurs fichiers externes en les listant les uns après les autres :

```yaml
include:
  - local: '/templates/cicd-template-1.yml'
  - remote: 'https://my.service.com/gitlab/templates/cicd-template-2.yml'
  - project: 'my-group/my-project'
    ref: main
    file: '/templates/cicd-template-3.yml'

stages:
  ...
```

Il est possible de redéfinir certains paramètres hérités de config externes, que ça soit au niveau global de la pipeline, ou au niveau local d'un job.

Dans ce cas, la valeur définie au sein du fichier de config aura la précédence sur celle provenant d'une inclusion externe.

Des configs importées via un `include` peuvent être réutilisées avec `extends` et `!reference`, mais pas avec les références YAML.

> [!warning]
> Le mécanisme d'inclusions externes ne doit pas être utilisé comme un mécanisme de sécurité permettant de contraindre l'utilisation de certains jobs. En effet, de part son fonctionnement, n'importe qui ayant accès au projet peut avoir accès aux fichiers inclus, qu'ils soient locaux, en remote où bien d'un autre projet. Ainsi il serait techniquement possible pour cette personne de récupérer le contenu de ces fichiers et de les modifier afin de contourner un ou plusieurs jobs.

> [!info]
> Il existe des services profitant de la fonctionnalité d'inclusion externe pour mettre à disposition des templates de jobs réutilisables.
>
> Voir [r2devops.io](https://r2devops.io), boite française.

#### Contrôler les inclusions externes
Il est possible de rajouter des règles qui conditionnent l'inclusion de configurations externes, avec les keywords `include:rules:if` et `include:rules:exists`. Les règles sont les mêmes qu'avec les [[Formation Gitlab CICD/Jour 1/3. Contexte d'exécution des pipelines#Règles d'exécution conditionnelle| rules des jobs]].

```yaml
include:
  - local: builds.yml
    rules:
      - if: $INCLUDE_BUILDS == "true"
  - local: deploys.yml
    rules:
      - if: $CI_COMMIT_BRANCH == "main"

test:
  stage: test
  script: exit 0
```

[\[ref\]](https://docs.gitlab.com/ee/ci/yaml/includes.html#use-rules-with-include)

#### Processus d'inclusion
Quelques notes sur le processus d'inclusions des fichiers externes :
- Les fichiers externes sont inclus les uns après les autres, dans l'ordre de leur déclaration
- Si un paramètre est défini dans plusieurs fichiers de configuration, la valeur du dernier fichier le définissant est celle utilisée

https://docs.gitlab.com/ee/ci/yaml/includes.html#merge-method-for-include

![[Formation Gitlab CICD/Jour 2/Attachements/Job inheritance process/Job inheritance process.svg]]

![[Formation Gitlab CICD/Jour 2/Attachements/Job inheritance process/Job inheritance process 3.svg]]