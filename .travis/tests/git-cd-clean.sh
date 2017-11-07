set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

# assert that new feature branch exists remote
git branch -a | grep "origin/feature/travis-test-$TRAVIS_JOB_NUMBER"

# delete feature branch on remote
git push origin :feature/travis-test-$TRAVIS_JOB_NUMBER

# assert that the feature branch not present on remote anymore
REMOTE_COUNT=`git branch -a | grep "origin/feature/travis-test-$TRAVIS_JOB_NUMBER" | wc -l`
if [ $REMOTE_COUNT != 0 ]; then
	echo "Feature Branch still found on remote"
	exit 1
fi

# call git-cd clean
git-cd clean

# assert the local feature branch is deleted
LOCAL_COUNT=`git branch -a | grep "feature/travis-test-$TRAVIS_JOB_NUMBER" | wc -l`
if [ $LOCAL_COUNT != 0 ]; then
	echo "Feature Branch still found locally"
	exit 1
fi

# change back to original workdir
cd -
