Todo's and features to implement
================================


Features
--------

* Check for updates initially on every command - not even sure if this is smart

Completing tests
----------------
* implement all the assertions mentioned in the ./travis bash scripts
* write a test which executes a git-cd init with different params and assert the config has changed
* write a test for git-cd clean
* write a test for git-cd compare
* write a test for git-cd status
* write a test for git-cd test
* write a test for git-cd finish without deleting the feature branch
* write two more release tests, one with tag number by file and one with tag number by date
* implement one of the three release test with an extra bash script execution
* try to write a test for git-cd version - at least it should always have a higher version than the pypi one
