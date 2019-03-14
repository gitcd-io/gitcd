set -e

CURRENT_VERSION=$(cat version.txt)
git-cd version | grep "You run git-cd in version $CURRENT_VERSION"
