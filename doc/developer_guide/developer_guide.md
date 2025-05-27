# Developer Guide

In this developer guide we explain how you can build this project.

**Install Poetry:**

```shell
sudo apt install python3-poetry
```

Or check for alternative ways at  
https://python-poetry.org/docs/#installation

**Prepare the virtual environment**

```shell
poetry env use python3
```

**Install dependencies:**

```shell
poetry install
```

**Install the Git commit hooks:**

```shell
poetry run -- pre-commit install
```

# Creating a Release

## Prerequisites

* Change log needs to be up to date  
* `unreleased` change log version needs to be up-to-date  
* Release tag needs to match package  

  For example:  
  * Tag: 0.4.0  
  * `poetry version -s`: 0.4.0  

## Preparing the Release

Run the following nox task in order to prepare the changelog:

```shell
nox -s release:prepare
```

## Triggering the Release

In order to trigger a release a new tag must be pushed to GitHub:

1. Create a local tag with the appropriate version number  
   ```shell
   git tag x.y.z
   ```
2. Push the tag to GitHub  
   ```shell
   git push origin x.y.z
   ```

## What to do if the release failed?

### The release failed during pre-release checks

1. Delete the local tag  
   ```shell
   git tag -d x.y.z
   ```
2. Delete the remote tag  
   ```shell
   git push --delete origin x.y.z
   ```
3. Fix the issue(s) which led to the failing checks  
4. Start the release process from the beginning  

### One of the release steps failed (Partial Release)

1. Check the GitHub action/workflow to see which steps failed  
2. Finish or redo the failed release steps manually  

> **Note**  
> **Scenario**: Publishing of the release on GitHub was successful but during the PyPI release, the upload step got interrupted.  
>
> **Solution**: Manually push the package to PyPI  

# Running Tests

You can execute unit tests with:

```shell
poetry run -- nox -s test:unit
```

You can execute integration tests with:

```shell
poetry run -- nox -s test:integration
```
