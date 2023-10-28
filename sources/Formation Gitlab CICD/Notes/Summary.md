#GitlabCI

https://www.youtube.com/playlist?list=PLn6POgpklwWrRoZZXv0xf71mvT4E0QDOF

- Qu'est-ce-que la CICD ?
- ~~gitlab CI vs github actions~~
	- ~~à voir selon les diffs~~
- gitlab CE vs EE
	- préciser que la formation ne sera que sur CE
		- la CE couvre déjà suffisament de points pour s'amuser pendant un moment
- runners and executors : [[Gitlab runners and executors]]
- variables
	- précédence
- architectures
- cache
- artifacts
- services
- sur quelles actions sont lancées les pipelines ? (push, MR créée ...?)
- job dependencies

xavki
- gitlab ci : contient les 3 étapes, *Continous Integration*, *Continuous Delivery*, *Continous Deployment*
- but : assurer et améliorer la qualité du code produit afin de gagner en efficacité et fiabilité
- Définitions :
	- pipeline : ensemble d'actions déclenchées de manière séquentielle lors de différentes actions effectuées sur du code d'un repo gitlab
		- déclenchée par trigger selon différentes actions ou par cron
		- découpé en stages
	- stage : étapes d'une pipeline, regroupement logique d'un ou plusieurs jobs
	- job : définition d'une tâche précise à effectuer, avec ses contraintes et conditions
	- runner : ressource permettant l'exécution des différentes étapes de la pipeline
		- sur une VM, Docker, K8S...
		- possibilité d'installer des softs supplémentaires nécessaires pour l'execution des jobs (npm, docker, ansible, kubectl...)
		- tagging pour indentifier les spécificités des runners
		- scope du runner (shared vs group vs project)
		- Cf [[Gitlab runners and executors]]
	- executor : type de runner adapté au job (ssh, docker, shell, k8s...)