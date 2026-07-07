#!/bin/bash

echo "=============================="
echo "Git Status"
echo "=============================="

git status

echo ""

read -p "Commit Message: " MESSAGE

echo ""

git add .

git commit -m "$MESSAGE"

git push origin main

echo ""

echo "Code pushed successfully."
