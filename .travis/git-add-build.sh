set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

echo travis-$TRAVIS_JOB_NUMBER >> README.rst
git commit -m "Add current build number" .
git push

# change back to original workdir
cd -
