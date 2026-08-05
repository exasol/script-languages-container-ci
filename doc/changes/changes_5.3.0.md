# 5.3.0 - 2026-08-05

## Summary

This release changes the filename of the exported Script-Languages-Container and updates to exaslct v4.3.1 and itde v6.5.1. Also, it contains some internal improvements.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| cryptography | PYSEC-2026-3552 | 49.0.0 | 50.0.0 |
| gitpython | GHSA-2f96-g7mh-g2hx | 3.1.50 | 3.1.51 |
| gitpython | GHSA-v396-v7q4-x2qj | 3.1.50 | 3.1.51 |
| gitpython | GHSA-956x-8gvw-wg5v | 3.1.50 | 3.1.51 |
| gitpython | GHSA-3rp5-jjmw-4wv2 | 3.1.50 | 3.1.53 |
| gitpython | GHSA-fjr4-x663-mwxc | 3.1.50 | 3.1.54 |
| gitpython | GHSA-6p8h-3wgx-97gf | 3.1.50 | 3.1.54 |
| gitpython | GHSA-r9mr-m37c-5fr3 | 3.1.50 | 3.1.54 |
| gitpython | GHSA-94p4-4cq8-9g67 | 3.1.50 | 3.1.55 |
| gitpython | GHSA-3f7w-8rr8-f37f | 3.1.50 | 3.1.57 |
| gitpython | GHSA-p538-c434-8v24 | 3.1.50 | 3.1.56 |
| msgpack | GHSA-6v7p-g79w-8964 | 1.2.0 | 1.2.1 |
| setuptools | PYSEC-2026-3447 | 82.0.1 | 83.0.0 |
| setuptools | PYSEC-2026-3447 | 82.0.1 | 83.0.0 |

## Refactoring

* #167: Updated to exasol-toolbox 10.2.1
* #171: Changed SLC export to use symlink and updated PTB to 10.4.0

## Dependency Updates

### `main`

* Updated dependency `click:8.4.1` to `8.4.2`
* Updated dependency `exasol-script-languages-container-tool:4.1.0` to `4.3.1`
* Updated dependency `gitpython:3.1.50` to `3.1.58`
* Updated dependency `setuptools:82.0.1` to `83.0.0`

### `dev`

* Updated dependency `exasol-toolbox:9.0.0` to `10.4.0`
* Updated dependency `pytest:9.1.0` to `9.1.1`
