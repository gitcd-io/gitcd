set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

git-cd start travis-$TRAVIS_JOB_NUMBER

# assert that new feature branch exists remote
git branch -a | grep "origin/feature/travis-$TRAVIS_JOB_NUMBER"

# change back to original workdir
cd -
