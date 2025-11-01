set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# Create an uncommitted change to test stash functionality
echo "Test uncommitted change for stash" >> README.rst

# Start a new feature branch with expect to handle the stash prompt
/usr/bin/expect <<EOD
set timeout 30
spawn git-cd start github-$env(GITHUB_RUN_NUMBER)-$env(PYTHON_VERSION)
expect {
    "You have uncommitted changes. Do you want me to stash them and re-apply after creating the new branch?" {
        send "yes\r"
        exp_continue
    }
    eof
}
EOD

# assert that new feature branch exists remote
git branch -a | grep "origin/feature/github-$GITHUB_RUN_NUMBER-$PYTHON_VERSION"

# assert the uncommitted changes are still there (stash pop was successful)
if ! git status --porcelain | grep -q "README.rst"; then
    echo "Expected uncommitted changes to be restored but found none"
    exit 1
fi

# clean up: discard the uncommitted changes
git checkout -- README.rst

# change back to original workdir
cd -
