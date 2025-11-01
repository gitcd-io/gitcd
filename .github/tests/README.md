# Integration Tests

This directory contains integration tests for git-cd.

## Test Repository

The tests use the repository at https://github.com/gitcd-io/travis-gitcd as a test repository.

## Running Tests Locally

To run the tests locally:

1. Clone the test repository:
   ```bash
   git clone https://github.com/gitcd-io/travis-gitcd.git ~/build/gitcd-io/travis-gitcd
   ```

2. Configure git:
   ```bash
   cd ~/build/gitcd-io/travis-gitcd
   git config user.email "test@example.com"
   git config user.name "Test User"
   ```

3. Set environment variable:
   ```bash
   export GITHUB_RUN_NUMBER=test-$(date +%s)
   ```

4. Run individual test scripts:
   ```bash
   bash .github/tests/git-cd-version.sh
   bash .github/tests/git-cd-init.sh
   # etc...
   ```

## GitHub Actions Setup

For the GitHub Actions workflow to work, you need to configure a secret named `GH_TEST_REPO_TOKEN` with a Personal Access Token that has write access to the `gitcd-io/travis-gitcd` repository.

To create a PAT:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (Full control of private repositories)
4. Copy the token
5. Add it as a repository secret named `GH_TEST_REPO_TOKEN`

## Test Scripts

- `git-cd-version.sh` - Test version command
- `git-cd-upgrade.sh` - Test upgrade functionality
- `git-cd-init.sh` - Test initialization
- `git-cd-start.sh` - Test starting a feature branch
- `git-add-build.sh` - Helper to add build commits
- `git-cd-refresh.sh` - Test refresh functionality
- `git-cd-review.sh` - Test creating pull requests
- `git-cd-finish.sh` - Test finishing a feature
- `git-cd-release.sh` - Test release process
- `git-cd-test.sh` - Test branch management
- `git-cd-compare.sh` - Test branch comparison
- `git-cd-clean.sh` - Test cleaning up branches
- `git-cd-init-release-date.sh` - Test date-based versioning init
- `git-cd-release-date.sh` - Test date-based release
- `git-cd-init-release-file.sh` - Test file-based versioning init
- `git-cd-release-file.sh` - Test file-based release
- `git-cd-subdirectory.sh` - Test running from subdirectories
- `git-reset.sh` - Helper to reset git state
