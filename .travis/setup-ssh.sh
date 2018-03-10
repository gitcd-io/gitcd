# setup ssh key for https://github.com/gitcd-io/travis-gitcd
declare -r SSH_FILE="$(mktemp -u $HOME/.ssh/XXXXX)"

openssl aes-256-cbc \
-K $encrypted_a8b48c8ad6aa_key \
-iv $encrypted_a8b48c8ad6aa_iv \
-in ".travis/travis_deploy_key.enc" \
-out "$SSH_FILE" -d

chmod 600 "$SSH_FILE" \
&& printf "%s\n" \
    "Host github.com" \
    "  IdentityFile $SSH_FILE" \
    "  LogLevel ERROR" >> ~/.ssh/config
