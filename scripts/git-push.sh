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

git push origin main

echo ""
echo "=============================="
echo "SUCCESS"
echo "=============================="
echo "✅ Repository synchronized successfully."