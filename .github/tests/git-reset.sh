set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# Save current branch name
CURRENT_BRANCH=$(git branch --show-current)

# Reset any local changes
git reset --hard

# Checkout master to allow cleanup
git checkout master

# Delete local feature branches that might exist
git branch -D "feature/github-$GITHUB_RUN_NUMBER-$PYTHON_VERSION" 2>/dev/null || true
git branch -D "test/github-$GITHUB_RUN_NUMBER-$PYTHON_VERSION" 2>/dev/null || true

# Reset master to origin
git reset --hard origin/master

# change back to original workdir
cd -
