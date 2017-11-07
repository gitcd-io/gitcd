set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

# start a feature
git-cd start travis-test-$TRAVIS_JOB_NUMBER

# assert that new feature branch exists remote
git branch -a | grep "origin/feature/travis-test-$TRAVIS_JOB_NUMBER"


# call git-cd clean
git-cd test

# assert the feature branch is checked out again
git status | grep "origin/feature/travis-test-$TRAVIS_JOB_NUMBER"

# assert there is no diff against the test branch


# change back to original workdir
cd -
