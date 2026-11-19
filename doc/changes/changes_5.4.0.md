# 5.4.0 - 2026-11-19

## Summary

 - #185: Dropped support for Python 3.10.

## Security Issues

This release fixes vulnerabilities by updating dependencies:

| Dependency | Vulnerability | Affected | Fixed in |
|------------|---------------|----------|----------|
| black | CVE-2026-114134 | 26.5.1 | 26.10.1 |
| certifi | PYSEC-2026-4320 | 2026.7.22 | 2026.10.18 |
| certifi | PYSEC-2026-4320 | 2026.7.22 | 2026.10.18 |
| filelock | CVE-2026-112940 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112913 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112907 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112938 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112936 | 3.32.2 | 4.0.9 |
| filelock | CVE-2026-112910 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112909 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112911 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112939 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112915 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112935 | 3.32.2 | 4.2.1 |
| filelock | CVE-2026-112908 | 3.32.2 | 4.2.1 |
| gitpython | PYSEC-2026-3984 | 3.1.58 | 3.1.60 |
| gitpython | PYSEC-2026-3982 | 3.1.58 | 3.1.60 |
| gitpython | PYSEC-2026-3984 | 3.1.58 | 3.1.60 |
| gitpython | PYSEC-2026-3785 | 3.1.58 | 3.1.59 |
| gitpython | PYSEC-2026-3786 | 3.1.58 | 3.1.59 |
| gitpython | PYSEC-2026-3787 | 3.1.58 | 3.1.59 |
| gitpython | PYSEC-2026-3788 | 3.1.58 | 3.1.59 |
| gitpython | PYSEC-2026-3786 | 3.1.58 | 3.1.59 |
| gitpython | PYSEC-2026-3787 | 3.1.58 | 3.1.59 |
| gitpython | PYSEC-2026-3788 | 3.1.58 | 3.1.59 |
| gitpython | PYSEC-2026-3837 | 3.1.58 | 3.1.59 |
| gitpython | PYSEC-2026-3837 | 3.1.58 | 3.1.59 |
| gitpython | CVE-2026-114145 | 3.1.58 | 3.2.1 |
| gitpython | CVE-2026-110859 | 3.1.58 | 3.2.0 |
| gitpython | CVE-2026-110858 | 3.1.58 | 3.2.0 |
| gitpython | CVE-2026-110856 | 3.1.58 | 3.2.0 |
| gitpython | CVE-2026-110857 | 3.1.58 | 3.2.0 |
| gitpython | CVE-2026-110855 | 3.1.58 | 3.2.0 |
| msgpack | CVE-2026-114613 | 1.2.1 | 1.2.3 |
| pyjwt | PYSEC-2026-4145 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4149 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4152 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4144 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4143 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4148 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4140 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4141 | 2.13.0 | 2.15.0 |
| pyjwt | PYSEC-2026-4147 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4151 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4150 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4142 | 2.13.0 | 2.14.0 |
| pyjwt | PYSEC-2026-4183 | 2.13.0 | 2.15.0 |
| pyjwt | GHSA-pxh4-856f-4h89 | 2.13.0 | 2.14.0 |
| pylint | CVE-2026-114608 | 4.0.6 | 4.0.9 |
| setuptools | GHSA-xmj3-9gf7-h52w | 83.0.0 | 84.1.0 |
| soupsieve | CVE-2026-126192 | 2.9.1 | 2.10.0 |
| soupsieve | CVE-2026-126193 | 2.9.1 | 3.0.2 |
| soupsieve | CVE-2026-126191 | 2.9.1 | 3.0.2 |
| tornado | PYSEC-2026-3928 | 6.5.7 | 6.5.8 |
| tornado | GHSA-chx6-46f5-w4vp | 6.5.7 | 6.5.9 |
| tornado | GHSA-c2m8-h5v5-343r | 6.5.7 | 6.5.9 |
| tornado | GHSA-3hv7-mjh2-fv65 | 6.5.7 | 6.5.9 |
| tornado | GHSA-wwv5-g3v4-889x | 6.5.7 | 6.5.8 |
| tornado | GHSA-8423-8fgw-73vq | 6.5.7 | 6.5.8 |
| tornado | CVE-2026-116577 | 6.5.7 | 6.6 |
| tornado | CVE-2026-115927 | 6.5.7 | 6.6 |
| tornado | CVE-2026-116578 | 6.5.7 | 6.6 |
| urllib3 | PYSEC-2026-4177 | 2.7.0 | 2.8.0 |
| urllib3 | PYSEC-2026-4176 | 2.7.0 | 2.8.0 |
| urllib3 | PYSEC-2026-4175 | 2.7.0 | 2.8.0 |
| virtualenv | PYSEC-2026-4011 | 21.7.1 | 21.7.12 |
| virtualenv | PYSEC-2026-4012 | 21.7.1 | 21.7.11 |
| virtualenv | PYSEC-2026-4014 | 21.7.1 | 21.7.12 |
| virtualenv | PYSEC-2026-4013 | 21.7.1 | 21.7.13 |
| virtualenv | PYSEC-2026-4011 | 21.7.1 | 21.7.12 |
| virtualenv | PYSEC-2026-4012 | 21.7.1 | 21.7.11 |
| virtualenv | PYSEC-2026-4013 | 21.7.1 | 21.7.13 |
| virtualenv | PYSEC-2026-4014 | 21.7.1 | 21.7.12 |
| virtualenv | PYSEC-2026-4382 | 21.7.1 | 21.14.9 |
| virtualenv | PYSEC-2026-4374 | 21.7.1 | 21.14.9 |
| virtualenv | PYSEC-2026-4380 | 21.7.1 | 21.14.9 |
| virtualenv | PYSEC-2026-4375 | 21.7.1 | 21.14.9 |
| virtualenv | PYSEC-2026-4384 | 21.7.1 | 21.14.7 |
| virtualenv | PYSEC-2026-4372 | 21.7.1 | 21.14.10 |
| virtualenv | PYSEC-2026-4377 | 21.7.1 | 21.14.9 |
| virtualenv | PYSEC-2026-4381 | 21.7.1 | 21.14.9 |
| virtualenv | PYSEC-2026-4378 | 21.7.1 | 21.14.9 |
| virtualenv | PYSEC-2026-4386 | 21.7.1 | 21.14.2 |
| virtualenv | PYSEC-2026-4387 | 21.7.1 | 21.14.2 |
| virtualenv | PYSEC-2026-4385 | 21.7.1 | 21.14.4 |
| virtualenv | PYSEC-2026-4379 | 21.7.1 | 21.14.9 |
| virtualenv | CVE-2026-113714 | 21.7.1 | 21.14.9 |
| virtualenv | CVE-2026-113717 | 21.7.1 | 21.14.9 |

## Documentation

 - #174: Fixed install command in user guide

## Dependency Updates

### `main`

* Updated dependency `click:8.4.2` to `8.5.0`
* Updated dependency `exasol-script-languages-container-tool:4.3.1` to `4.4.0`
* Updated dependency `gitpython:3.1.58` to `3.2.1`
* Updated dependency `pygithub:2.9.1` to `2.10.0`
* Updated dependency `setuptools:83.0.0` to `84.2.1`

### `dev`

* Updated dependency `exasol-toolbox:10.4.0` to `10.5.0`
* Updated dependency `pytest:9.1.1` to `9.2.0`
* Updated dependency `pytest-mock:3.15.1` to `3.17.0`
