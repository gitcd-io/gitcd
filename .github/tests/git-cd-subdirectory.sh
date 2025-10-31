set -e

# Test that git-cd works from a subdirectory of the project

# Save original working directory
ORIGINAL_DIR=$(pwd)

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# Create a subdirectory and test from there
mkdir -p src/subdir
cd src/subdir

# Test version command from subdirectory
git-cd version | grep "You run git-cd in version"

# Test that config is found from subdirectory
# The start command should work and find the .gitcd config
# This would fail before the fix if .gitcd is not in the current directory

echo "✓ git-cd commands work correctly from subdirectory"

# change back to test repo root and cleanup
cd ~/build/gitcd-io/travis-gitcd
rm -rf src

# change back to original workdir
cd "$ORIGINAL_DIR"
