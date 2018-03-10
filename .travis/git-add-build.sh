set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

echo travis-$TRAVIS_JOB_NUMBER >> README.rst
git commit -m "Add current build number: $TRAVIS_JOB_NUMBER" .
git push

# change back to original workdir
cd -
