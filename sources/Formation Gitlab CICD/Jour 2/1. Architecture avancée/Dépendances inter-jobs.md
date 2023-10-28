---
title: "Dépendances inter-jobs"
tags:
- GitlabCI
---
À l'aide du keyword `[job]:needs`, il est possible de définir un DAG (*Directed Acyclic Graph*, *Graphe Orienté Acyclique*). Cette fonctionnalité permet de sortir de l'exécution séquentielle classique où les stages s'exécutent les uns après les autres, selon la configuration prédéfinie.

En définissant un DAG, on indique des dépendances entre des jobs, ce qui permet d'accélérer l'exécution de la pipeline. Un job qui a certaines dépendances d'indiquées va s'exécuter dès lors que le(s) job(s) dont il dépend auront été exécuté(s) avec succès.

## Impact sur la récupération des artefacts

Tout comme [`[job]:dependencies`](https://docs.gitlab.com/ee/ci/yaml/#dependencies), lorsqu'un job déclare une ou plusieurs dépendance(s), il ne va récupérer que les artefacts produits par le(s) job(s) dont il dépend.

Il est possible par ailleurs de ne récupérer aucun artefacts des dépendances, tout en conservant celles-ci :

```yaml
test job:
  stage: test
  needs:
    - job: "build job"
      artifacts: false
```

[\[ref\]](https://docs.gitlab.com/ee/ci/yaml/#needsartifacts)

```yaml
stages:
  - build
  - test
  - package
  - upload

build macos 10:
  stage: build
  script:
    - echo "Building in macOS"
    - mkdir -p binaries
    - touch binaries/macos-10
    - sleep $((1 + $RANDOM % 10))
  artifacts:
    paths:
      - binaries/

build macos 11:
  stage: build
  script:
    - echo "Building in macOS"
    - mkdir -p binaries
    - touch binaries/macos-11
    - sleep $((1 + $RANDOM % 10))
  artifacts:
    paths:
      - binaries/

build debian 10:
  stage: build
  script:
    - echo "Building in debian"
    - mkdir -p binaries
    - touch binaries/debian-10
    - sleep $((1 + $RANDOM % 10))
  artifacts:
    paths:
      - binaries/

build debian 11:
  stage: build
  script:
    - echo "Building in debian"
    - mkdir -p binaries
    - touch binaries/debian-11
    - sleep $((1 + $RANDOM % 10))
  artifacts:
    paths:
      - binaries/

test macos 10:
  stage: test
  script:
    - echo "Testing in macOS"
    - ls -lA binaries/
    - mkdir -p tests
    - touch tests/macos-10
  needs:
    - build macos 10
  artifacts:
    paths:
      - tests/

test macos 11:
  stage: test
  script:
    - echo "Testing in macOS"
    - ls -lA binaries/
    - mkdir -p tests
    - touch tests/macos-11
  needs:
    - build macos 11
  artifacts:
    paths:
      - tests/

test debian 10:
  stage: test
  script:
    - echo "Testing in debian"
    - ls -lA binaries/
    - mkdir -p tests
    - touch tests/debian-10
  needs:
    - build debian 10
  artifacts:
    paths:
      - tests/

test debian 11:
  stage: test
  script:
    - echo "Testing in debian"
    - ls -lA binaries/
    - mkdir -p tests
    - touch tests/debian-11
  needs:
    - build debian 11
  artifacts:
    paths:
      - tests/

package macos:
  stage: package
  script:
    - echo "Packaging macOS"
    - ls -lA binaries/
    - mkdir -p packages
    - tar -czvf packages/macos.tar.gz binaries
  needs:
    - build macos 10
    - build macos 11
  artifacts:
    paths:
      - packages/

package debian:
  stage: package
  script:
    - echo "Packaging debian"
    - ls -lA binaries/
    - mkdir -p packages
    - tar -czvf packages/debian.tar.gz binaries
  needs:
    - build debian 10
    - build debian 11
  artifacts:
    paths:
      - packages/

upload:
  stage: upload
  script:
    - echo "Uploading generated binaries"
    - ls -lA binaries/
    - ls -lA packages/
    - ls -lA tests/
```
