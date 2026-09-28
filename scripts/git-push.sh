#!/bin/bash

set -e

echo "========================================================"
echo "                 GIT PUSH UTILITY"
echo "========================================================"
echo ""

# Always execute Git commands from repository root
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

echo "Repository Root"
echo "--------------------------------------------------------"
echo "$REPO_ROOT"
echo ""

echo "Repository Status"
echo "--------------------------------------------------------"
git status
echo ""

# Stage all changes
echo "Adding files..."
git add -A

# Exit if nothing changed
if git diff --cached --quiet; then
    echo ""
    echo "No local changes detected."
    echo "Repository is already synchronized."
    exit 0
fi

echo ""
echo "Changes to be committed"
echo "--------------------------------------------------------"
git diff --cached --stat
echo ""

read -p "Commit Message: " MESSAGE
echo ""

# Prevent empty commit message
if [ -z "$MESSAGE" ]; then
    echo "Commit message cannot be empty."
    exit 1
fi

echo "Creating commit..."
git commit -m "$MESSAGE"

echo ""
echo "Synchronizing with GitHub..."
echo "--------------------------------------------------------"

git pull --rebase origin main

echo ""
echo "Pushing changes..."
echo "--------------------------------------------------------"

if git push origin main; then

    echo ""
    echo "========================================================"
    echo "      GITHUB PUSH SUCCESSFUL"
    echo "========================================================"

else

    echo ""
    echo "Push rejected. Repository changed during push."
    echo "Retrying..."

    git pull --rebase origin main
    git push origin main

    echo ""
    echo "========================================================"
    echo "GITHUB PUSH SUCCESSFUL (AFTER RETRY)"
    echo "========================================================"

fi

echo ""
echo "Latest Commit"
echo "--------------------------------------------------------"
git log -1 --oneline

echo ""
echo "Current Branch"
echo "--------------------------------------------------------"
git branch --show-current

echo ""
echo "Repository Status"
echo "--------------------------------------------------------"
git status

echo ""
echo "========================================================"
echo "Repository synchronized successfully."
echo "========================================================"