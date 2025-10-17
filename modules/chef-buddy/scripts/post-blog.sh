#!/usr/bin/env bash
# Blog posting script
# Usage: ./post-blog.sh <post-title>

set -e

if [ -z "$1" ]; then
    echo '{"error": "No blog post title provided"}'
    exit 1
fi

POST_TITLE="$1"

# Simulate posting the blog
printf '{"status": "success", "message": "Your blog post '\''%s'\'' was posted successfully!"}\n' "$POST_TITLE"
