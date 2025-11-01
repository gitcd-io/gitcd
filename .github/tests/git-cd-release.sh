set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# Ensure we're on master with a clean state
git fetch origin
git checkout master
git reset --hard origin/master

# git-cd finish with deleting the feature branch
/usr/bin/expect <<EOD
spawn git-cd release
expect "Whats the current tag number you want to deliver?"
send "$GITHUB_RUN_NUMBER-$PYTHON_VERSION\n"
expect "What message your new tag should have?"
send "New GitHub Release $GITHUB_RUN_NUMBER-$PYTHON_VERSION\n"
expect
EOD

# assert that the new tag exists

# change back to original workdir
cd -