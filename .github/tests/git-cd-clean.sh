set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# assert that new feature branch exists remote
git branch -a | grep "origin/feature/github-test-$GITHUB_RUN_NUMBER"

# delete feature branch on remote
git push origin :feature/github-test-$GITHUB_RUN_NUMBER

# assert that the feature branch not present on remote anymore
REMOTE_COUNT=`git branch -a | grep "origin/feature/github-test-$GITHUB_RUN_NUMBER" | wc -l`
if [ $REMOTE_COUNT != 0 ]; then
	echo "Feature Branch still found on remote"
	exit 1
fi

# call git-cd clean
/usr/bin/expect <<EOD
spawn git-cd clean
expect "Do you want me to delete those branches locally?"
send "yes\n"
expect
EOD

# assert the local feature branch is deleted
LOCAL_COUNT=`git branch -a | grep "feature/github-test-$GITHUB_RUN_NUMBER" | wc -l`
if [ $LOCAL_COUNT != 0 ]; then
	echo "Feature Branch still found locally"
	exit 1
fi

# change back to original workdir
cd -
