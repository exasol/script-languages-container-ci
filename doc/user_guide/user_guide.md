# exaslc-ci CLI — User Guide

**EXASLC_CI** is a command-line tool to build, test, scan and deploy Exasol’s Script-Languages Containers  
in a GitHub CI environment. See https://github.com/exasol/script-languages-release for more information about  
Script-Languages-Containers. Under the main entrypoint `exaslc-ci`, it exposes a set of commands to  
orchestrate your CI pipeline steps.
## Installation & Prerequisites

1. Python 3.10+  
2. Install the package:

   ```shell
   pip install exaslc-ci
   ```

3. Ensure a valid GitHub token in your CI (`GITHUB_TOKEN`) if using GitHub outputs.

---

### Required CI files

The CLI commands expect to be called within a Script-Languages directory, which must contain the following directories and files:

```
├── flavors
│   ├── flavor_a
│   │   ├── flavor_base
│   │   │   ├──...
│   │   ├── ci.json
│   │   ...
├── build_config.json
```

There must exist at least one flavor directory (`flavor_a` in the example above) with the respective `ci.json` file.
The `build_config.json` contains build parameter, which are independent of the flavors.

#### Flavor `ci.json`

This file contains flavor specific build information:

- `build_runner`: The Github build runner to be used for building the Script-Languages-Container of the respective flavor
- `test_config`: Test specific build information:
  - `default_test_runner`: The Github runner to be used for running the tests
  - `test_sets`: A set of tests which should run within the same matrix build
    - `name`: The name of the test set
    - `folders`: The list of folders with tests within the test container (usually `test_container/tests/test`) which will be executed. If not empty, the enty `generic_language_tests` should be empty.
    - `goal`: The release goal, to be used for running the tests. The release goal is defined in the `build_steps.py`. The release goal needs to be exported during the command `export-and-scan-vulnerabilities`. Currently only two goals are exported and can be used for the tests: `release` and `base_test_build_run`. The reason the goal `base_test_build_run` is supported, are the linker namespace tests. 
    - `generic_language_tests`: A list of generic language tests. If not empty, the entry `folders` should be empty.
    - `test_runner`: The specific Github runner for the test set. If set, it overwrites the `default_test_runner`. It allows the usage of more expansive Github runner (for example GPU runner) for specific tests
    - `accelerator`: This option is forwarded to `exaslct`'s `run-db-test` command. It allows starting the docker-db with an accelerator enabled.
Here is an example file:

```json
{
  "build_runner": "ubuntu-22.04",
  "test_config": {
    "default_test_runner": "ubuntu-22.04",
    "test_sets": [
      {
        "name": "integration-test",
        "folders": ["some_tests"],
        "goal": "release",
        "generic_language_tests": []
      },
      {
        "name": "integration-test-for-base_test_build_run",
        "folders": ["some_tests"],
        "goal": "base_test_build_run",
        "generic_language_tests": []
      },
      {
        "name": "integration-test-gpu",
        "folders": ["gpu_tests"],
        "goal": "release",
        "generic_language_tests": [],
        "test_runner": "int-linux-x64-4core-gpu-t4-ubuntu24.04-1",
        "accelerator": "nvidia"
      }
    ]
  }
}

```

#### `build_config.json`

This file contains flavor independent information:
- `ignore_paths`: A list of folders which will avoid building the Script-Languages-Container during CI
- `docker_build_repository`: A Docker repository where the intermediate build docker images will be uploaded. This allows inspection of the Docker containers later, if needed.
- `docker_release_repository`: A Docker repository where the release docker images will be uploaded.
- `test_container_folder`: The folder name containing the test container.
- 
```json
{
    "ignore_paths": ["doc"],
    "docker_build_repository": "exadockerci4/script-languages-build-cache",
    "docker_release_repository": "exasol/script-languages",
    "test_container_folder": "test_container"
}

```

## How it Fits in the Big Picture

The following diagram shows how this project is used within the Script-Languages-Container CI/CD pipeline.  
The auto-generated GitHub workflows call the CLI commands of this project to construct build matrices or to trigger the single build steps.

![SLC CI](./img/slc_ci.png)

---

## Global Usage

```shell
Usage: exaslc-ci [OPTIONS] COMMAND [ARGS]...

  EXASLC_CI - Exasol Script Languages Continuous Integration

Options:
  --help    Show this message and exit.
```

Run `exaslc-ci COMMAND --help` for detailed options per command.

---

## Commands

### get-flavors

Searches for all available container “flavors” (e.g. `standard-EXASOL-all-python-3.10`, `template-Exasol-all-r-4`)  
and writes the result as a JSON array to a GitHub Actions output variable.

**Usage**

```shell
exaslc-ci get-flavors --github-output-var FLAVOR_LIST
```

**Options**

- `--github-output-var TEXT`  
  Name of the GitHub Actions output variable to store the resulting JSON array. **(Required)**

**Example (GitHub Actions)**

```yaml
- name: Get available flavors
  run: exaslc-ci get-flavors --github-output-var flavors
  env:
    GITHUB_OUTPUT: ${{ github.output }}
```

---

### get-test-matrix

Generates a test matrix for a given flavor and writes it into a GitHub Actions output variable.

**Usage**

```shell
exaslc-ci get-test-matrix --flavor standard-EXASOL-all-python-3.10 --github-output-var MATRIX
```

**Options**

- `--flavor TEXT`  
  The container flavor to generate the test matrix for. **(Required)**
- `--github-output-var TEXT`  
  GitHub Actions output variable name. **(Required)**

**Example**

```yaml
- name: Generate test matrix
  run: exaslc-ci get-test-matrix --flavor standard-EXASOL-all-python-3.10 --github-output-var matrix
  env:
    GITHUB_OUTPUT: ${{ github.output }}
```

---

### get-build-runner

Resolves which GitHub runner labels (e.g. `ubuntu-latest`/`windows-latest`) should be used to build a given flavor.

**Usage**

```shell
exaslc-ci get-build-runner --flavor standard-EXASOL-all-python-3.10 --github-output-var RUNNER_LABELS
```

**Options**

- `--flavor TEXT`  
  Flavor identifier. **(Required)**
- `--github-output-var TEXT`  
  GitHub Actions output variable. **(Required)**

---

### check-if-build-needed

Checks whether a new build is needed by comparing the current branch vs. a base branch.  
Outputs a boolean (`true`/`false`) to a GitHub variable.

**Usage**

```shell
exaslc-ci check-if-build-needed \
  --flavor standard-EXASOL-all-python-3.10 \
  --branch feature/XYZ \
  --base-ref main \
  --remote origin \
  --github-output-var NEED_BUILD
```

**Options**

- `--flavor TEXT`
- `--branch TEXT`
- `--base-ref TEXT`
- `--remote TEXT`
- `--github-output-var TEXT`

---

### export-and-scan-vulnerabilities

Performs a full CI pipeline step: builds the container, exports it, scans for vulnerabilities, and pushes results to the Docker Hub build cache.

**Usage**

```shell
exaslc-ci export-and-scan-vulnerabilities \
  --flavor standard-EXASOL-all-python-3.10 \
  --branch feature/XYZ \
  --commit-sha abc123 \
  --docker-user ${{ secrets.DOCKER_USER }} \
  --docker-password ${{ secrets.DOCKER_PASS }} \
  --github-output-var VULN_SCAN_RESULT
  --release/--no-release
```

**Options**

- `--flavor TEXT`
- `--branch TEXT`
- `--commit-sha TEXT`
- `--docker-user TEXT`
- `--docker-password TEXT`
- `--github-output-var TEXT`
- `--release/--no-release`: If True, the "docker_release_repository" entry of `build_config.json` will be used for uploading the Script-Languages container image. Otherwise, the "docker_release_repository" will be used.

#### Internals

1. Build the container  
2. Run a security scan  
3. Export the container  
4. Push results  

---

### prepare-test-container

Builds a test container image from a given commit, then pushes it to your registry.  
The test container must contain its own build description (Dockerfile), the test SQL data and the UDF tests.

**Usage**

```shell
exaslc-ci prepare-test-container \
  --commit-sha abc123 \
  --docker-user ${{ secrets.DOCKER_USER }} \
  --docker-password ${{ secrets.DOCKER_PASS }}
```

**Options**

- `--commit-sha TEXT`
- `--docker-user TEXT`
- `--docker-password TEXT`

---

### run-tests

Runs integration tests inside a previously built/test container.

**Usage**

```shell
exaslc-ci run-tests \
  --flavor standard-EXASOL-all-python-3.10 \
  --slc-directory ./build/slc \
  --test-set-name full \
  --docker-user ${{ secrets.DOCKER_USER }} \
  --docker-password ${{ secrets.DOCKER_PASS }}
```

**Options**

- `--flavor TEXT`
- `--slc-directory PATH`  
  Directory where the built SLC file resides.
- `--test-set-name TEXT`
- `--docker-user TEXT`
- `--docker-password TEXT`

---

## Troubleshooting & Support

If you encounter errors or missing functionality, please open a GitHub ticket:  
https://github.com/exasol/script-languages-container-ci/issues/new/choose
