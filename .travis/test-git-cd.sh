# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

git-cd start travis-$TRAVIS_JOB_NUMBER
if [ $? != 0 ]; then
    exit 1
fi

# change back to original workdir
cd -