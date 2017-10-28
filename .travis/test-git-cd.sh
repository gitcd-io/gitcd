# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd
git checkout master
git pull origin master

git-cd start travis-$TRAVIS_JOB_NUMBER
echo $?
# change back to original workdir
cd -