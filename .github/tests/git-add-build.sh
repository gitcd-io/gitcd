set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

echo github-$GITHUB_RUN_NUMBER >> README.rst
git commit -m "Add current build number: $GITHUB_RUN_NUMBER" .
git push

# change back to original workdir
cd -
