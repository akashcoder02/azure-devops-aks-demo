#!/bin/bash

set -e

echo "=============================="
echo "Git Status"
echo "=============================="

git status
echo ""

read -p "Commit Message: " MESSAGE
echo ""

echo "Adding files..."
git add .

if git diff --cached --quiet; then
    echo "Nothing to commit."
else
    git commit -m "$MESSAGE"
fi

echo ""
echo "=============================="
echo "Syncing with GitHub"
echo "=============================="

git pull --rebase origin main

echo ""
echo "=============================="
echo "Pushing to GitHub"
echo "=============================="

git push origin main#!/bin/bash

set -e

echo "========================================================"
echo "                 GIT PUSH UTILITY"
echo "========================================================"
echo ""

echo "Repository Status"
echo "--------------------------------------------------------"
git status
echo ""

# Stage all changes
git add .

# Exit if nothing changed
if git diff --cached --quiet; then
    echo "No local changes detected."
    echo "Repository is already up to date."
    exit 0
fi

read -p "Commit Message: " MESSAGE
echo ""

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
    echo "           GITHUB PUSH SUCCESSFUL"
    echo "========================================================"

else

    echo ""
    echo "Push rejected. Repository changed during push."
    echo "Retrying automatically..."

    git pull --rebase origin main
    git push origin main

    echo ""
    echo "========================================================"
    echo "     GITHUB PUSH SUCCESSFUL (AFTER RETRY)"
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

echo ""
echo "=============================="
echo "SUCCESS"
echo "=============================="
echo "✅ Repository synchronized successfully."