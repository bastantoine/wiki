---
title: "Gestion des secrets avec Hashicorp Vault"
tags:
- GitlabCI
---

Vault est un outil développé par Hashicorp pour gérer des secrets et données sensibles.

Pour pouvoir récupérer des données stockées dans Vault depuis l'extérieur, il faut s'authentifier, et donc avoir un jeu de credentials.

Si l'idée d'utiliser Vault pour ne plus stocker aucune donnée sensible dans les variables de CICD, la nécessité de stocker des credentials pour pouvoir accéder aux secrets de Vault est un peu contradictoire.

Il est possible d'utiliser un JWT généré par Gitlab pour s'authentifier auprès de Vault, et pouvoir ensuite récupérer les credentials.

## Mécanisme d'authentification
Lors de la préparation d'un job, Gitlab va fournir un JWT dédié pour le job (`$CI_JOB_JWT`) , avec des informations sur le job en question, et son contexte (project, branche...).

Parmi les nombreuses méthodes d'authentification dont dispose Vault, il est possible de s'authentifier avec un JWT. Ainsi on peut, dans la CICD, utiliser ce JWT pour s'authentifier, et par la suite récupérer des données sensibles.

```json
{
  "jti": "c82eeb0c-5c6f-4a33-abf5-4c474b92b558",
  "iss": "gitlab.example.com",
  "iat": 1585710286,
  "nbf": 1585798372,
  "exp": 1585713886,
  "sub": "job_1212",
  "namespace_id": "1",
  "namespace_path": "mygroup",
  "project_id": "22",
  "project_path": "mygroup/myproject",
  "user_id": "42",
  "user_login": "myuser",
  "user_email": "myuser@example.com",
  "pipeline_id": "1212",
  "pipeline_source": "web",
  "job_id": "1212",
  "ref": "auto-deploy-2020-04-01",
  "ref_type": "branch",
  "ref_path": "refs/heads/auto-deploy-2020-04-01",
  "ref_protected": "true",
  "environment": "production",
  "environment_protected": "true"
}
```

Côté Vault, on peut restreindre l'accès à des espaces selon des informations contenues dans le JWT. Il est possible, par exemple, de restreindre l'accès à l'espace `my-project/production` aux JWT émis au sein du projet `my-group/my-project`, soit ceux dont `JWT['project_path'] = "mygroup/myproject"`.

Le process est le suivant
1. Configuration de Vault pour accepter l'authentification JWT depuis Gitlab, pour l'espace voulu, et restreindre les accès à l'espace selon des informations contenues dans le JWT
2. Lors du lancement du job, Gitlab va créer un JWT qu'il va fournir au runner pour qu'il soit accessible par le job
3. Le job va l'utiliser pour s'authentifier sur Vault
4. Vault va vérifier que le JWT est bien valide (pas expiré, bien émis par Gitlab et correctement signé)
5. Vault va vérifier que les politiques d'accès en place permettent bien l'accès à l'espace demandé avec ce JWT
6. Vault va générer un token qu'il va fournir au job
7. Le job va utiliser ce token pour récupérer des données stockées sur Vault

![[Formation Gitlab CICD/Jour 2/Attachements/Vault/Vault.svg]]

> [!note]
> L'utilisation des JWT via la variables `$CI_JOB_JWT` est dépréciée et est prévue d'être remplacée par les ID token pour permettre l'utilisation d'OpenID Connect.

[\[ref\]](https://docs.gitlab.com/ee/ci/secrets/)

## Utilisation des ID tokens pour l'authentification à des services externes
Le problème de stockage de credentials au sein des variables de CICD est assez courant, et n'est pas limité qu'à Vault.

Dès lors qu'un job souhaite utiliser un service extérieur nécessitant de l'authentification, il est nécessaire de stocker quelque part accessible par le job les données nécessaires à l'authentification.

Certains services permettent de s'authentifier à l'aide de token JWT, et plus précisément en utilisant des ID tokens et le mécanisme OpenID Connect. 

Gitlab peut générer ces ID tokens, et permettre l'authentification à différents services, comme AWS, GCP ou Azure.

[\[ref\]](https://docs.gitlab.com/ee/ci/cloud_services/index.html) [\[ref\]](https://docs.gitlab.com/ee/ci/yaml/index.html#id_tokens)