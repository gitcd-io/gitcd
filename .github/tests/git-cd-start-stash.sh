set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# Create an uncommitted change
echo "Test uncommitted change for stash" >> README.rst

# Verify there are uncommitted changes
if ! git status --porcelain | grep -q "README.rst"; then
    echo "Expected uncommitted changes but found none"
    exit 1
fi

# Start a new feature branch with stash
/usr/bin/expect <<EOD
spawn git-cd start github-stash-$GITHUB_RUN_NUMBER-$PYTHON_VERSION
expect "You have uncommitted changes. Do you want me to stash them and re-apply after creating the new branch?"
send "yes\n"
expect
EOD

# Assert that new feature branch exists remote
git branch -a | grep "origin/feature/github-stash-$GITHUB_RUN_NUMBER-$PYTHON_VERSION"

# Assert we are on the new feature branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
EXPECTED_BRANCH="feature/github-stash-$GITHUB_RUN_NUMBER-$PYTHON_VERSION"
if [ "$CURRENT_BRANCH" != "$EXPECTED_BRANCH" ]; then
    echo "Expected to be on branch $EXPECTED_BRANCH but was on $CURRENT_BRANCH"
    exit 1
fi

# Assert the uncommitted changes are still there (stash pop was successful)
if ! git status --porcelain | grep -q "README.rst"; then
    echo "Expected uncommitted changes to be restored but found none"
    exit 1
fi

# Verify the stash is empty (changes were popped)
STASH_COUNT=$(git stash list | wc -l)
if [ $STASH_COUNT != 0 ]; then
    echo "Expected stash to be empty but found $STASH_COUNT entries"
    exit 1
fi

# Clean up: discard the uncommitted changes
git checkout -- README.rst

# Delete the test branch
git checkout master
git branch -D "feature/github-stash-$GITHUB_RUN_NUMBER-$PYTHON_VERSION" 2>/dev/null || true
git push origin --delete "feature/github-stash-$GITHUB_RUN_NUMBER-$PYTHON_VERSION" 2>/dev/null || true

# change back to original workdir
cd -
