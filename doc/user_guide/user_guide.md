# exaslc-ci CLI — User Guide

**EXASLC_CI** is a command-line tool to build, test, scan and deploy Exasol’s Script-Languages-Containers (SLCs)
in a GitHub CI environment. See https://github.com/exasol/script-languages-release for more information about  
SLCs. Under the main entrypoint `exaslc-ci`, it exposes a set of commands to  
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
File `build_config.json` contains build parameters, which are independent of the flavors.

#### Flavor `ci.json`

This file contains flavor-specific build information:

- `build_runner`: The Github build runner to be used for building the SLC of the respective flavor
- `test_config`: Test-specific build information:
  - `default_test_runner`: The Github runner to be used for running the tests
  - `test_sets`: A set of tests which should run within the same matrix build
    - `name`: The name of the test set
    - `folders`: The list of folders with tests within the test container (usually `test_container/tests/test`) which will be executed.
    - `goal`: The release goal, to be used for running the tests, either `release` or `base_test_build_run`, see details below.
    - `generic_language_tests`: A list of generic language tests.
    - `test_runner`: The specific Github runner for the test set. If set, it overwrites the `default_test_runner` enabling to use different Github runners for running specific tests, e.g. for minimizing costs.
    - `accelerator`: SLC-CI forwards this option to `exaslct` command [run-db-test](https://github.com/exasol/script-languages-container-tool/blob/main/doc/user_guide/user_guide.md#testing-with-an-accelerator), example value `nvidia`.

Only one of either `folders` or `generic_language_tests` should have a non-empty value.

Release goals are defined by the return values of method `get_build_step()` in file `build_steps.py` of each flavor. Currently SLC-CI command `export-and-scan-vulnerabilities` only exports two goals: `release` and `base_test_build_run`. The second goal is for running tests regarding linker namespaces.

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

This file contains flavor-independent information:
- `ignore_paths`: Changes of the PR / Push in these directories will _not_ trigger building and testing the SLC.
- `docker_build_repository`: A Docker repository where slc-ci uploads the intermediate docker images to. This allows inspecting and reusing the Docker containers later.
- `docker_release_repository`: A Docker repository where the final release docker images will be uploaded.
- `test_container_folder`: Name of the folder containing the test container.
```json
{
    "ignore_paths": ["doc"],
    "docker_build_repository": "exadockerci4/script-languages-build-cache",
    "docker_release_repository": "exasol/script-languages",
    "test_container_folder": "test_container"
}

```

## How it Fits in the Big Picture

The following diagram shows how this project is used within the SLC CI/CD pipeline.  
The auto-generated GitHub workflows call the CLI commands of this project to obtain build matrices or to trigger individual build steps.

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

Performs a full CI pipeline step: builds the container, exports it, scans for vulnerabilities, and pushes results to the Docker Hub build/release cache.

**Usage**

```shell
exaslc-ci export-and-scan-vulnerabilities \
  --flavor standard-EXASOL-all-python-3.10 \
  --branch feature/XYZ \
  --commit-sha abc123 \
  --docker-user ${{ secrets.DOCKER_USER }} \
  --docker-password ${{ secrets.DOCKER_PASS }} \
  --github-output-var VULN_SCAN_RESULT \
  --release
```

**Options**

- `--flavor TEXT`
- `--branch TEXT`
- `--commit-sha TEXT`
- `--docker-user TEXT`
- `--docker-password TEXT`
- `--github-output-var TEXT`
- `--release`: If specified, then run `export-and-scan-vulnerabilities` in mode _release_, always re-building all Docker images and publishing the images to "docker_release_repository". Otherwise only rebuild outdated Docker images and publish them to "docker_build_repository".

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
