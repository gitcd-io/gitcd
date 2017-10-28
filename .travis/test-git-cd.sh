#. .travis/exit-on-error.sh

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

git-cd start travis-$TRAVIS_JOB_NUMBER
#exitOnError()
if [ $? != 0 ]; then
    exit $?
fi

# change back to original workdir
cd -
