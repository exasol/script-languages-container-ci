# 3.0.0 - 2025-06-06

This release removes support for the AWS Code build CI.
Also, it adds the rebuild option to command `export_and_scan_vulnerabilities` and pushes the docker image to the docker release repository if the build is triggered on the main branch.

## Refactorings

 - #102: Replace branch config with rebuild option
 - #103: Push to release docker repository when running CI on main branch
 - #105: Remove legacy exasol_script_languages_container_ci module
