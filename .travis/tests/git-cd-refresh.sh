set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# merge master
git-cd refresh

# change back to original workdir
cd -
