set -e

CURRENT_VERSION=$(cat version.txt)
echo "Current version var is: $CURRENT_VERSION\n"
echo "You run git-cd in version $CURRENT_VERSION\n"

/usr/bin/expect <<EOD
spawn git-cd version
expect "You run git-cd in version $CURRENT_VERSION\n"
expect
EOD
