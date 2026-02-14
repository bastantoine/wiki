#GitlabCI

https://docs.gitlab.com/runner/

Runner : 

## SaaS vs self-hosted
https://docs.gitlab.com/ee/ci/runners/

## Scope of runners
https://docs.gitlab.com/ee/ci/runners/runners_scope.html
-   Shared runners are available to all groups and projects in a GitLab instance.
-   Group runners are available to all projects and subgroups in a group.
-   Project runners are associated with specific projects. Typically, project runners are used by one project at a time.

## Compatibility
https://docs.gitlab.com/runner/executors/#compatibility-chart

## Runner execution flow
```mermaid
sequenceDiagram
    participant gl as GitLab
    participant runner as GitLab Runner
    participant exec as Executor
    opt registration
      runner ->>+ gl: POST /api/v4/runners with registration_token
      gl -->>- runner: Registered with runner_token
    end
    loop job requesting and handling
      runner ->>+ gl: POST /api/v4/jobs/request with runner_token
      gl -->>+ runner: job payload with job_token
      runner ->>+ exec: Job payload
      exec ->>+ gl: clone sources with job_token
      exec ->>+ gl: download artifacts with job_token
      exec -->>- runner: return job output and status
      runner -->>- gl: updating job output and status with job_token
    end
```
[\[source\]](https://docs.gitlab.com/runner/#runner-execution-flow)

## Démos
Lancer un job et faire un `docker ps`/`ps -faux` en parallèle