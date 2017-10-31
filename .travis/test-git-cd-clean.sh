set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

git-cd start travis-clean-$TRAVIS_JOB_NUMBER

# assert that new feature branch exists remote
git branch -a | grep "origin/feature/travis-clean-$TRAVIS_JOB_NUMBER"

git push origin :feature/travis-clean-$TRAVIS_JOB_NUMBER

git-cd clean
# change back to original workdir
cd -
