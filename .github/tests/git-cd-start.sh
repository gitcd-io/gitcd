set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

git-cd start github-$GITHUB_RUN_NUMBER

# assert that new feature branch exists remote
git branch -a | grep "origin/feature/github-$GITHUB_RUN_NUMBER"

# change back to original workdir
cd -
