# 2.0.0 - 2025-05-23

This release provides the new module (exasol.slc_ci) and the new CLI script (exasolslc-ci), which will be used in Github workflows to build, test, push and release Script-Languages-Container.

## Refactorings

 - #76: Updated pyproject.toml and PTB

## Features

 - #75: Implemented CI for Github workflows - check if build needed
 - #82: Implement CI for Github workflows - build-and-export
 - #83: Implement CI for Github workflows - run-tests
 - #87: Use remote part for base ref option
 - #89: Implement CI for Github workflows - get-test-matrix
 - #91: Add accelerator to test configuration


## Bugs

 - #79: Fixed print docker images
