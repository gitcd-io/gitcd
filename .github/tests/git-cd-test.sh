set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# start a feature
git-cd start github-test-$GITHUB_RUN_NUMBER

# assert that new feature branch exists remote
git branch -a | grep "origin/feature/github-test-$GITHUB_RUN_NUMBER"


# call git-cd clean
git-cd test

# assert the feature branch is checked out again
git status | grep "origin/feature/github-test-$GITHUB_RUN_NUMBER"

# assert there is no diff against the test branch


# change back to original workdir
cd -
