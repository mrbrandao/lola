#!/usr/bin/env bash
# Blog creation script
# Usage: ./new-blog.sh <post-title>

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
ROOT_DIR="$(readlink -f "${SCRIPT_DIR}/../../../")"
TEMPLATE="${SCRIPT_DIR}/../templates/blog-template.md"

if [ -z "$1" ]; then
    echo '{"error": "No blog post title provided"}'
    exit 1
fi

# Convert the title to lowercase and snake_case (replace spaces with underscores)
POST_TITLE="$1"

# Create the blog directory if it doesn't exist
mkdir -p "${SCRIPT_DIR}/../../../content/blog"

# Get current date in RFC3339 format
TODAY=$(date --rfc-3339=seconds)

# Define the new blog file path
BLOG_FILE="${SCRIPT_DIR}/../../../content/blog/${POST_TITLE}.md"

# Check if template exists
if [ ! -f "${TEMPLATE}" ]; then
    echo '{"error": "Template file not found"}'
    exit 1
fi

# Copy the template to the new blog file
cp "${TEMPLATE}" "${BLOG_FILE}"

# Calculate relative path from root for display
BLOG_FILE_ABSOLUTE="$(readlink -f "${BLOG_FILE}")"
RELATIVE_PATH="${BLOG_FILE_ABSOLUTE#${ROOT_DIR}/}"

# Return JSON with the filename and date
printf '{"today": "%s", "blog-post": "%s"}\n' "${TODAY}" "${RELATIVE_PATH}"

