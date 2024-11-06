# Gitlab CI Linter

This project aims to provide linting for Gitlab CI files, specifically the shell scripts within the jobs.  

This is done by calling the CI Lint API endpoint, thus verifying the the CI. Then using the response of the lint call to obtain the fully expanded CI, extracting the script sections and running [Shellcheck](https://github.com/koalaman/shellcheck) to lint the scripts.  

Since Gitlab itself is used to obtain the expanded CI, both `include` and `!reference` are supported.

# Authentication

You will need a token capable of calling the [CI Lint API endpoint](https://docs.gitlab.com/ee/api/lint.html). See the [API Authentication docs](https://docs.gitlab.com/ee/api/rest/#authentication) for what your options are in this regard.  
Note that CI job tokens are NOT able to call this endpoint.

# Installation

A CI ready Docker image can be found in the [Container Registy](https://gitlab.com/SydneyChadwick/gitlab-ci-linter/container_registry).  
As the intention here is mainly for CI usage, this should be the primary use case.

However a PyPi package can also be found in the [Package Registry](https://gitlab.com/SydneyChadwick/gitlab-ci-linter/-/packages).  
Release versions are also available on [pypi.org](https://pypi.org/project/gitlab-ci-script-linter/)  
__NB:__ Note that shellcheck must be installed separately in this case

# Usage

```
usage: gl-ci-lint [-h] [-v] -t TOKEN [-b BRANCH] [-o OUTPUT] [-p PROJECTID] [-e SEVERITY] [-s SHELL] [-u URL]
                  [--debug] [--sast]
                  [file]

Collate .gitlab-ci.yml files into script sections for linting

positional arguments:
  file                  CI file that you want to lint (Default .gitlab-ci.yml)

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -t TOKEN, --token TOKEN
                        API Token with permissions to call CI Lint API
  -b BRANCH, --branch BRANCH
                        Git branch to use for include.local (Default: CI_COMMIT_BRANCH)
  -o OUTPUT, --output OUTPUT
                        Directory in which to write expanded scripts (Default: scripts)
  -p PROJECTID, --projectid PROJECTID
                        ID of the Gitlab project (Default $CI_PROJECT_ID)
  -e SEVERITY, --severity SEVERITY
                        Minimum serverity of errors to consider for shellcheck run (Default: warning)
  -s SHELL, --shell SHELL
                        Default path to be used when adding shebang to script file (Default: /bin/sh)
  -u URL, --url URL     Gitlab API URL (Default $CI_API_V4_URL)
  --debug               Enable debug output, primarily printing script files
  --sast                Indicate if Gitlab SAST jobs should be scanned. False if not present
  ```

## Indicating the shell to lint

Shellcheck requires a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) in order to be capable of linting accurately.  
This tool will inject a shebang at the start of each produced script.

There are a number of ways to set this, from lowest to highest priority:
* Do nothing - the tool defaults to `/bin/sh`
* --shell - this will be used globally for the run
* Add a shebang as a string (in quotes!) in the script

For a CI file with multiple jobs possibly using different images, you can use a combination of `--shell` to set a default and the in-script version to override the default for jobs that should not use the default.

## Samples

### Test current project .gitlab-ci.yml

This will test the CI of the current repository.

```
"Verify CI":
  image: registry.gitlab.com/sydneychadwick/gitlab-ci-linter:latest
  stage: verify
  script:
    - "#!/bin/ash"
    - "# shellcheck shell=dash"
    - "# shellcheck disable=SC3036" # echo -e is supported by ash, but not dash. So disabling this rule.
    - gl-ci-lint --shell /bin/bash --token "$CI_TEST_TOKEN" ".gitlab-ci.yml"
  rules:
    - if: $CI_COMMIT_BRANCH && $CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH
      changes:
        paths: 
          - .gitlab-ci.yml
        compare_to: 'main'
    - if: $CI_COMMIT_BRANCH && $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
```

### Testing a CI component

For CI template/component projects, this can be used to test a component file

```
"Test CI component":
  image: registry.gitlab.com/sydneychadwick/gitlab-ci-linter:latest
  stage: verify
  script:
    - gl-ci-lint --shell /bin/bash --token "$CI_TEST_TOKEN" "templates/component.yml"

```

### Testing multiple CI component files

If there are multiple components to test, you can reuse script sections.  
A parallel matrix could also be beneficial, but has not been tested 

```
.ci-test:
  image: registry.gitlab.com/sydneychadwick/gitlab-ci-linter:latest
  stage: verify
  script:
    - gl-ci-lint --shell /bin/bash --token "$CI_TEST_TOKEN" "$CI_FILE"

"Test Component1":
  extends: .ci-test
  variables:
    CI_FILE: templates/component1.yml

"Test Component2":
  extends: .ci-test
  variables:
    CI_FILE: templates/component2.yml
```

# Shellcheck directives

Shellcheck supports adding [directives](https://github.com/koalaman/shellcheck/wiki/Directive) as comments in shell scripts in order to modify behaviour.  

This can be done in CI scripts, as long as the full comment is in quotes.  
As an example, the sample below of a job running on Alpine with collapsible sections uses directives to:
  * Indicates that the shell in use is `ash`
  * That we know it will be treated as `dash`, to suppress [SC2187](https://www.shellcheck.net/wiki/SC2187)
  * Disables the warning that `echo -e` is not supported on `dash`

```yml
script:
    - "#!/bin/ash"
    - "# shellcheck shell=dash"
    - "# shellcheck disable=SC3036" # echo -e is supported by ash, but not dash. So disabling this rule.
    - echo -e "\e[0Ksection_start:`date +%s`:config[collapsed=true]\r\e[0K\e[1;93mConfiguration"
    - echo "Hello world"
    - echo -e "\e[0Ksection_end:`date +%s`:config\r\e[0K"
```

# Acknowledgments

This project was developed with the support and funding of [AfriGIS](https://www.afrigis.co.za/). Their commitment to innovation and excellence made this tool possible. Special thanks to the entire team for their invaluable contributions and support throughout the development process.