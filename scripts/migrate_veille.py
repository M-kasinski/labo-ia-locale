#!/usr/bin/env python3
"""Migrate articles from veille-ia to site, adding category field."""

import os
import re
import sys

VEILLE_DIR = "/Users/m.kasinski/labs/H_agent/veille-ia/src/content/blog"
SITE_DIR = "/Users/m.kasinski/labs/H_agent/site/src/content/blog"

def add_category(filepath, category):
    """Add or update category in frontmatter YAML."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has category
    if re.search(r'^category:\s*', content, re.MULTILINE):
        print(f"  SKIP (has category): {os.path.basename(filepath)}")
        return False

    # Insert category after pubDate line
    lines = content.split('\n')
    new_lines = []
    inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and line.startswith('pubDate:'):
            # Match indentation (usually no indent in frontmatter)
            new_lines.append(f'category: "{category}"')
            inserted = True

    if not inserted:
        # Fallback: insert after --- opening
        for i, line in enumerate(lines):
            new_lines2 = []
            for j, l in enumerate(lines):
                new_lines2.append(l)
                if j == 0 and l.strip() == '---':
                    # Find a good insertion point - after pubDate or before closing ---
                    pass
            new_lines = new_lines2

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

    return True

def main():
    # Get list of files in site (to skip duplicates)
    site_files = set(os.listdir(SITE_DIR))

    # Get veille-ia files to migrate
    veille_files = sorted([f for f in os.listdir(VEILLE_DIR) if f.endswith(('.md', '.mdx'))])

    migrated = 0
    skipped = 0

    for filename in veille_files:
        src_path = os.path.join(VEILLE_DIR, filename)
        dst_path = os.path.join(SITE_DIR, filename)

        if filename in site_files:
            print(f"  SKIP (duplicate): {filename}")
            skipped += 1
            continue

        # Copy file
        import shutil
        shutil.copy2(src_path, dst_path)

        # Add category: veille
        add_category(dst_path, "veille")
        migrated += 1

    print(f"\nMigrated: {migrated}, Skipped (duplicates): {skipped}")

if __name__ == '__main__':
    main()
