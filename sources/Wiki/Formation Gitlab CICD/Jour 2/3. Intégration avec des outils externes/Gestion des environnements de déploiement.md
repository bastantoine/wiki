---
title: "Gestion des environnements de déploiement"
tags:
- GitlabCI
---

## Gestion des environnements de déploiement

Gitlab offre la possibilité de suivre les différents déploiements des applications sur différents environnements.

Cela permet d'avoir l'historique des déploiements sur les différents environnements, ainsi que permettre de suivre ce qui est déployé.

[\[ref\]](https://docs.gitlab.com/ee/ci/environments/)

### Création d'un déploiement

Pour créer un déploiement il est nécessaire d'associer le job ayant réalisé le déploiement sur un environnement à cet environnement, en utilisant le keyword `[job]:environment`.

Le lancement du job va créer un nouveau déploiement sur l'environnement en question.

```yaml
deploy app:
  environment: production
  script: echo "Deploying app"
```

> [!note]
> Si un job spécifie un environnement qui n'existe pas, cet environnement est créé au sein du projet.

> [!note]
> L'implémentation du déploiement en lui même est laissé libre. Un projet peut vouloir déployer via Ansible tandis qu'un autre va déployer avec Flux ou ArgoCD sur un cluster Kubernetes.

[\[ref\]](https://docs.gitlab.com/ee/ci/yaml/#environment)

### Visualisation des environnements

Les différents environnements actifs sont listés au sein de la page *Deployments > Environments*.

On y retrouve, pour chacun des environnements actifs, le dernier déploiement en date, quelques infos sur celui-ci (commit déployé, date du déploiement...), ainsi que la possibilité d'agir dessus (y acceder, le stopper...).

![[Formation Gitlab CICD/Jour 2/Attachements/Environnements/Interface/Env infos.png]]

Le clic sur un environnement permet d'afficher la liste des différents déploiements qui y ont eu lieu, ainsi que la possibilité d'un rollback sur ces différents déploiements.

![[Formation Gitlab CICD/Jour 2/Attachements/Environnements/Interface/Env details.png]]

Lorsque le job de déploiement vers un environnement est lancé dans une pipeline associée à une merge request, la page de résumé de la pipeline indique le lien vers le déploiement en question.

![[Formation Gitlab CICD/Jour 2/Attachements/Environnements/Interface/Merge request.png]]

### Lien avec l'application déployée
En règle générale, les applications qui sont déployées via une pipeline de CICD sont accessibles par une URL via une navigateur.

Il est possible de lier un environnement à son URL, afin de faciliter l'accès à l'application déployée. Pour cela il suffit de fournir l'URL du déploiement au sein du job ayant contribué à déployer l'application :

```yaml
deploy app:
  environment:
    name: production
    url: https://my-app.com
  script: echo "Deploying app"
```

[\[ref\]](https://docs.gitlab.com/ee/ci/yaml/index.html#environmenturl)

![[Formation Gitlab CICD/Jour 2/Attachements/Environnements/Interface/Env infos with link.png]]

![[Formation Gitlab CICD/Jour 2/Attachements/Environnements/Interface/Env details with link.png]]

![[Formation Gitlab CICD/Jour 2/Attachements/Environnements/Interface/Merge request with link.png]]

### Environnement dynamiques

Il est possible d'utiliser des variables dans les noms et URL des environnements. Ainsi, en utilisant des variables de CICD spécifiques à chaque pipeline, on peut créer des environnements dynamiques.

```yaml
deploy review app:
  stage: deploy
  script: echo "Deploying app"
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_ENVIRONMENT_SLUG.example.com
  rules:
    - if: $CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH
```

### Arrêt d'un environnement

Durant le cycle de vie d'une application, on peut vouloir l'arrêter pour différentes raisons. Lorsque son déploiement est suivi par Gitlab, il est possible de définir un job réalisant l'arrêt de l'application.

Pour ce faire, il faut définir un job en charge d'effectuer l'arrêt, l'associer à l'environnement en question, indiquer qu'il est en charge de l'arrêt via le keyword `[job]:environment:action`, et en le liant au job chargé du déploiement avec `[jbo]:environment:on_stop` :

```yaml
deploy_review:
  stage: deploy
  script:
    - echo "Deploy a review app"
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_ENVIRONMENT_SLUG.example.com
    on_stop: stop_review

stop_review:
  stage: deploy
  script:
    - echo "Remove review app"
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  when: manual
```

[\[ref\]](https://docs.gitlab.com/ee/ci/yaml/index.html#environmenton_stop) [\[ref\]](https://docs.gitlab.com/ee/ci/yaml/index.html#environmentaction)

### Déploiement dans un cluster Kubernetes

Gitlab permet la connexion de clusters Kubernetes afin de réaliser la gestion d'applications déployées sur ces clusters directement via Gitlab.

Une fois le cluster connecté, il est possible d'utiliser des versionner les manifests des applications à déployer et utiliser les pipelines CICD Gitlab pour gérer leur cycle de vie.