# Not a YAML
Develop your CI/CD pipelines as code, in the same programming language as your application.

Modeling `.gitlab-ci.yml` after GitLab's official [documentation](https://docs.gitlab.com/ee/ci/yaml/)

```mermaid
classDiagram
  class GitLabJob {
    - name: string
    - script: string
    - artifacts: list of Artifact
    - dependencies: list of GitLabJob
    - environmentVariables: map
    - whenToRun: string
    - resources: ResourceRequirements
    - timeouts: TimeDuration
    - retryLimit: int
    - caches: list of Cache
    - services: list of Service
  }

  class Artifact {
    - name: string
    - paths: list of string
  }

  class ResourceRequirements {
    - cpuLimit: string
    - memoryLimit: string
  }

  class TimeDuration {
    - duration: int
  }

  class Cache {
    - key: string
    - paths: list of string
  }

  class Service {
    - name: string
    - image: string
  }

  GitLabJob --|> Artifact
  GitLabJob --|> ResourceRequirements
  GitLabJob --|> TimeDuration
  GitLabJob --|> Cache
  GitLabJob --|> Service


  
