# change workdir to travis-gitcd
. exit-on-error.sh

cd ~/build/claudio-walser/travis-gitcd

git-cd start travis-$TRAVIS_JOB_NUMBER
exitOnError()

# change back to original workdir
cd -
