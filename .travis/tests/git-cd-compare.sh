set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

# call git-cd compare and compare it to the test branch
git-cd compare test

# assert there is no diff

# change back to original workdir
cd -
