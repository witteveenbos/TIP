#!/bin/bash
# Git setup script for devcontainer
# This script ensures git works properly in the container

echo "Setting up git configuration..."

# Ensure workspace ownership
sudo chown -R vscode:vscode /workspace 2>/dev/null || true

# Configure git safe directories
git config --global --add safe.directory /workspace
git config --global --add safe.directory '*'

# Set basic git config if not inherited from host
if [ -z "$(git config --global user.name 2>/dev/null)" ]; then
    echo "Setting default git user name..."
    git config --global user.name "Dev Container User"
fi

if [ -z "$(git config --global user.email 2>/dev/null)" ]; then
    echo "Setting default git user email..."
    git config --global user.email "dev@container.local"
fi

# Disable file mode checking to avoid permission issues
git config --global core.filemode false

# Set proper permissions for git directories
if [ -d "/workspace/.git" ]; then
    echo "Fixing git directory permissions..."
    sudo chown -R vscode:vscode /workspace/.git 2>/dev/null || true
    chmod -R u+rw /workspace/.git 2>/dev/null || true
fi

# Test git functionality
echo "Testing git functionality..."
cd /workspace
if git status >/dev/null 2>&1; then
    echo "✅ Git is working correctly!"
else
    echo "❌ Git test failed. Attempting additional fixes..."
    
    # Additional troubleshooting
    git config --global --replace-all safe.directory '*'
    sudo chown -R vscode:vscode /workspace
    
    # Try again
    if git status >/dev/null 2>&1; then
        echo "✅ Git is now working after additional fixes!"
    else
        echo "❌ Git still not working. Manual intervention may be needed."
        echo "Current git config:"
        git config --list --global | grep -E "(safe\.directory|user\.|core\.filemode)"
        echo "Workspace ownership:"
        ls -la /workspace/.git 2>/dev/null || echo "No .git directory found"
    fi
fi

echo "Git setup complete."