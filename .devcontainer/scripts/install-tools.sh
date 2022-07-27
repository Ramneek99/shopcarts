# !/bin/bash

echo "Creating aliases for new tools..."
echo "alias ic='/usr/local/bin/ibmcloud'" >> $HOME/.bash_aliases
echo "alias kc='/usr/local/bin/kubectl'" >> $HOME/.bash_aliases
echo "alias ku='/usr/local/bin/kustomize'" >> $HOME/.bash_aliases
echo "alias kns='kubectl config set-context --current --namespace'" >> $HOME/.bash_aliases

# Platform specific installs
if [ $(uname -m) == aarch64 ]; then
    echo "Installing YQ for ARM64..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm64
    sudo chmod a+x /usr/local/bin/yq
else
    echo "Installing YQ for x86_64..."
    sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
    sudo chmod a+x /usr/local/bin/yq
fi;