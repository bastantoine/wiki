#GitlabCI

# Pipeline creation control
https://docs.gitlab.com/ee/ci/yaml/workflow.html

# Job running control
https://docs.gitlab.com/ee/ci/jobs/job_control.html

## En utilisant le keyword `rules`
Utiliser le keyword `rules` pour indiquer dans quel cas ajouter ou non le job dans la pipeline.

Les règles sont évaluées de haut en bas, et la première qui match est utilisée pour savoir si le job est ajouté ou non.

Conditions :
- [`rules:if`](https://docs.gitlab.com/ee/ci/yaml/index.html#rulesif): expression booléenne ([ref](https://docs.gitlab.com/ee/ci/jobs/job_control.html#cicd-variable-expressions))
	- Match si l'expression booléenne est vérifiée
- [`rules:changes`](https://docs.gitlab.com/ee/ci/yaml/index.html#ruleschanges): une liste de fichiers ou glob pattern
	- Match si au moins un fichier identifié par un des pattern contient des changements
	- Notes :
		- Si plusieurs règles de matchs sont fournies, elles sont évaluées avec un *OR*
		- Possibilité de comparer par rapport à une ref donnée avec [`rules:changes:compare_to`](https://docs.gitlab.com/ee/ci/yaml/index.html#ruleschangescompare_to)
> [!warning]
> `rules:changes` ne doit être utilisé que pour des pipelines de branches ou de MR. Dans tous les autres cas ces règles sont vérifiées dans tous les cas puisqu'elles ne sont pas associées à un event Git push.
- [`rules:exists`](https://docs.gitlab.com/ee/ci/yaml/index.html#rulesexists): une liste de fichiers ou glob pattern
	- match si au moins un des fichiers identifié par une des règles existe
- Notes sur les règles :
	- Si il y a une combinaison de plusieurs règles, elles doivent toutes être vérifiées pour que le job soit ajouté :
		- Si `when: never`, le job n'est pas ajouté si toutes les conditions sont vérifiées 

Si aucune règle n'a match, le job n'est pas ajouté dans la pipeline. Pour l'ajouter si rien ne match, ajouter `- when: on_success` comme dernière rule.

> [!warning]
> Dans le cas où la dernière règle inclue une clause `when`, (sauf `when: never`), on peut avoir deux pipelines simultanées, pour le push et la MR, qui peuvent être trigger par le même event.

### À propos du keyword `when`
Ce keyword indique sous quelle condition lancer un job :
-   `on_success`: exécute le job uniquement lorsque tous les jobs des étapes précédentes réussissent, ou sont considérés comme réussis via l’utilisation `allow_failure: true`.
-   `on_failure` : exécuter la tâche uniquement lorsque au moins une tâche à une étape antérieure échoue.
-   `always` : exécuter le job quel que soit le statut des jobs aux étapes précédentes.
-   `manual`: lancement du job manuellement.
-   `delayed`: retarder l’exécution d’un job pendant une durée spécifiée.
-   `never` : ne lance pas le job dans ce cas
https://blog.stephane-robert.info/post/gitlab-rules/

Il est possible de mixer `when`au niveau du job et `rules:when`. Dans le cas où les deux sont présents, le `rules:when` sera préféré.

### Lancer des jobs manuellement

`when: manual`

Deux types de jobs manuels:
1. jobs bloquants : `allow_failure: false`
	- Pipeline en status *bloqué* tant que le job n'a pas été lancé manuellement
2. jobs optionel: `allow_failure: true`


## En utilisant les keywords `only`/`except`
`only` sert à indiquer dans quels cas ajouter le job
`except` sert à indiquer dans quels cas ne pas ajouter le job

Conditions possibles :
- [`only:refs` / `except:refs`](https://docs.gitlab.com/ee/ci/yaml/index.html#onlyrefs--exceptrefs): quand ajouter, ou non, le job selon le nom de la branche où la pipeline est lancée, ou bien le type de pipeline lancée
	- Si uniquement `only` / `except` sont utilisés, c'est équivalent à `only:refs` / `except:refs`
- [`only:variables` / `except:variables`](https://docs.gitlab.com/ee/ci/yaml/index.html#onlyvariables--exceptvariables) : quand ajouter, ou non, le job à la pipeline selon la valeur d'une ou plusieurs variables
> [!note]
> `only:refs`/`except:refs` sont à éviter au profit de  `rules:if` lors de check sur les refs ou la valeur de variables CICD
- [`only:changes` / `except:changes`](https://docs.gitlab.com/ee/ci/yaml/index.html#onlychanges--exceptchanges): quand ajouter, ou non, le job si des changements ont été détectés sur un ou plusieurs fichiers identifiés par un ou plusieurs patterns fournis
	- Si plusieurs patterns sont fournis, ils sont évaluées avec un *OR*
	- Ne peut être utilisé que pour les refs qui sont liés à un git push, soit `branches`, `external_pull_requests`, ou `merge_requests`. Évalué à true pour toutes les autres refs.
> [!note]
> `only:changes` / `except:changes` sont à éviter au profit de  `rules:changes` lors de check sur le changement de fichiers

## Default value

Si aucune règle de contrôle n'est fournie avec `rules` ou `only`/`except`, une valeur par défaut est mise sur le job pour ne le lancer que pour les branches et les tags, soit un équivalent de :

```yaml
job:
	script: echo "test"
	only:
	- branches
	- tags
```