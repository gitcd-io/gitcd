set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

git-cd start travis-$TRAVIS_JOB_NUMBER

# change back to original workdir
cd -