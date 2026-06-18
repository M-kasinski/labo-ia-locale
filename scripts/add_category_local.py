#!/usr/bin/env python3
"""Add category: 'local' to existing site articles that don't have it."""

import os
import re

SITE_DIR = "/Users/m.kasinski/labs/H_agent/site/src/content/blog"

def add_category_local(filepath):
    """Add category: 'local' after pubDate line in frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has category
    if re.search(r'^category:\s*', content, re.MULTILINE):
        return False

    lines = content.split('\n')
    new_lines = []
    inserted = False

    for line in lines:
        new_lines.append(line)
        if not inserted and line.startswith('pubDate:'):
            new_lines.append('category: "local"')
            inserted = True

    if inserted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        return True
    return False

def main():
    count = 0
    for filename in sorted(os.listdir(SITE_DIR)):
        if not filename.endswith(('.md', '.mdx')):
            continue
        filepath = os.path.join(SITE_DIR, filename)
        if add_category_local(filepath):
            print(f"  Added category: {filename}")
            count += 1

    print(f"\nTotal: {count} articles updated")

if __name__ == '__main__':
    main()
