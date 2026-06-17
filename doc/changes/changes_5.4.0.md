# 5.4.0 - 2026-06-17

## Summary

This release fixes a problem with the `build_name` for the CI and contains internal improvements.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| cryptography | GHSA-537c-gmf6-5ccf | 48.0.0 | 48.0.1 |
| pip | PYSEC-2026-196 | 26.1.1 | 26.1.2 |
| pyjwt | PYSEC-2026-179 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-175 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-177 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-178 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-177 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-179 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-176 | 2.12.1 | 2.13.0 |
| pyjwt | PYSEC-2026-178 | 2.12.1 | 2.13.0 |
| tornado | CVE-2026-49854 | 6.5.5 | 6.5.6 |
| tornado | CVE-2026-49853 | 6.5.5 | 6.5.6 |
| tornado | CVE-2026-49855 | 6.5.5 | 6.5.6 |
| tornado | GHSA-pw6j-qg29-8w7f | 6.5.5 | 6.5.7 |

## Refactorings

 - #157: Adapted to build_name changes in ITDE and SLCT

## Internal

 - #155: Updated PTB to 8.2.0
 - #158: Updated PTB to 9.0.0

## Dependency Updates

### `main`

* Updated dependency `click:8.3.3` to `8.4.1`
* Updated dependency `exasol-script-languages-container-tool:4.0.3` to `4.1.0`

### `dev`

* Updated dependency `exasol-toolbox:7.0.0` to `9.0.0`
* Updated dependency `pytest:9.0.3` to `9.1.0`