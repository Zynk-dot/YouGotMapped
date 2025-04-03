#!/bin/bash

# This script replaces ALL mentions of your old email (from suuucyyehcy)
# with your new identity

OLD_EMAIL="kgao2472@gmail.com"
CORRECT_NAME="Kevin Gao"
CORRECT_EMAIL="kevingao0618@gmail.com"

echo "🔁 Rewriting Git history to replace $OLD_EMAIL with $CORRECT_EMAIL and normalize name..."

git filter-branch --env-filter '
if [ "$GIT_COMMITTER_EMAIL" = "'"$OLD_EMAIL"'" ]
then
    export GIT_COMMITTER_NAME="'"$CORRECT_NAME"'"
    export GIT_COMMITTER_EMAIL="'"$CORRECT_EMAIL"'"
fi
if [ "$GIT_AUTHOR_EMAIL" = "'"$OLD_EMAIL"'" ]
then
    export GIT_AUTHOR_NAME="'"$CORRECT_NAME"'"
    export GIT_AUTHOR_EMAIL="'"$CORRECT_EMAIL"'"
fi
' --tag-name-filter cat -- --branches --tags

echo "✅ Done rewriting!"
echo "⚠️  Now push with force to update GitHub:"
echo "    git push --force --all"
echo "    git push --force --tags"
