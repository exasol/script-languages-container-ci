# 5.1.2 - 2026-05-13

## Summary

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| black | CVE-2026-32274 | 25.12.0 | 26.3.1 |
| cryptography | CVE-2026-26007 | 46.0.4 | 46.0.5 |
| cryptography | CVE-2026-34073 | 46.0.4 | 46.0.6 |
| cryptography | CVE-2026-39892 | 46.0.4 | 46.0.7 |
| requests | CVE-2026-25645 | 2.32.5 | 2.33.0 |
| urllib3 | CVE-2026-44431 | 2.6.3 | 2.7.0 |
| urllib3 | CVE-2026-44432 | 2.6.3 | 2.7.0 |
| tornado | GHSA-78cv-mqj4-43f7 | 6.5.4 | 6.5.5 |
| tornado | CVE-2026-31958 | 6.5.4 | 6.5.5 |
| tornado | CVE-2026-35536 | 6.5.4 | 6.5.5 |
| pytest | CVE-2025-71176 | 7.4.4 | 9.0.3 |
| gitpython | CVE-2026-42215 | 3.1.46 | 3.1.47 |
| gitpython | CVE-2026-42284 | 3.1.46 | 3.1.47 |
| gitpython | CVE-2026-44244 | 3.1.46 | 3.1.49 |
| gitpython | GHSA-mv93-w799-cj2w | 3.1.46 | 3.1.50 |
| pip | CVE-2026-6357 | 26.0.1 | 26.1 |
| pygments | CVE-2026-4539 | 2.19.2 | 2.20.0 |
| pyjwt | CVE-2026-32597 | 2.11.0 | 2.12.0 |

## Internal

 - Relocked dependencies
 - Updated PTB to version 6.1.1
 - #150: Removed explicit dependency to "requests"
 - #152: Resolved vulnerabilities and updated PTB

## Dependency Updates

### `main`

* Updated dependency `click:8.3.1` to `8.3.3`
* Updated dependency `exasol-script-languages-container-tool:4.0.1` to `4.0.3`
* Updated dependency `gitpython:3.1.46` to `3.1.50`
* Updated dependency `pygithub:2.8.1` to `2.9.1`
* Updated dependency `setuptools:82.0.0` to `82.0.1`

### `dev`

* Updated dependency `exasol-toolbox:5.1.1` to `7.0.0`
* Updated dependency `pytest:7.4.4` to `9.0.3`