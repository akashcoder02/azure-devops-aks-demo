#!/bin/bash

echo "=============================="
echo "Git Status"
echo "=============================="

git status
echo ""

read -p "Commit Message: " MESSAGE
echo ""

git add .

if git diff --cached --quiet; then
    echo "Nothing to commit."
else
    git commit -m "$MESSAGE"
fi

echo ""
echo "Pushing to GitHub..."
echo ""

if git push origin main; then
    echo ""
    echo "✅ Code pushed successfully."
else
    echo ""
    echo "❌ Push failed."
    echo ""
    echo "Run:"
    echo "git pull --rebase origin main"
    echo "git push origin main"
    exit 1
fi