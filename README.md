# Not a YAML
Develop your CI/CD pipelines as code, in the same programming language as your application.

Modeling `.gitlab-ci.yml` after GitLab's official [documentation](https://docs.gitlab.com/ee/ci/yaml/)

```mermaid
graph TD
  start[Start]
  start --> stages[Stages]
  stages --> before_script[Before Script]
  stages --> after_script[After Script]
  stages --> image[Docker Image]
  stages --> cache[Cache]
  stages --> include[Include]
  stages --> default[Default]
  stages --> pages[Pages]
  stages --> workflow[Workflow]
  stages --> jobs[Jobs]
  jobs --> rules[Rules]
  jobs --> only_except[Only / Except]
  jobs --> dependencies[Dependencies]
  jobs --> artifacts[Artifacts]
  jobs --> needs[Needs]
  jobs --> environment[Environment]
  jobs --> resource_group[Resource Group]
  jobs --> ...
  jobs --> ...
