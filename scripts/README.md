# Obsidian → Astro Publish Workflow

A Python script that takes a finished blog post from Obsidian, uploads its images to Cloudflare R2, and copies the post to your Astro project.

## Prerequisites

- Python 3
- `boto3` and `python-dotenv` installed globally:
  ```bash
  pip3 install boto3 python-dotenv
  ```
- A Cloudflare R2 bucket with public access enabled

## Setup

Add the following to `.env.local` in your Astro project root:

```bash
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key_id
R2_SECRET_ACCESS_KEY=your_secret_access_key
R2_BUCKET_NAME=blog-images
R2_PUBLIC_URL=https://pub-xxxxxxxxxxxx.r2.dev

OBSIDIAN_PUBLISHED_PATH=/path/to/vault/Blog/published
OBSIDIAN_IMAGES_PATH=/path/to/vault/Blog/_images
ASTRO_POSTS_PATH=/path/to/astro/src/content/posts
```

## Obsidian Folder Structure

```
Blog/
  _templates/
    post-template.md     ← Templater template
  drafts/
    my-post.md           ← Work in progress
  published/
    my-post.md           ← Ready to publish
  _images/
    my-post/             ← Auto-created by Templater
      banner.png
      diagram.png
```

## Usage

When a post is ready, move it from `drafts/` to `published/` in Obsidian, then run:

```bash
python3 scripts/publish.py my-post-title
```

The script will:
1. Read `Blog/published/my-post-title.md`
2. Find all `![[image.png]]` Obsidian-style image links
3. Upload each image from `Blog/_images/my-post-title/` to R2
4. Rewrite image links to public R2 URLs
5. Save the finished file to `content/posts/my-post-title.mdx`

## Obsidian Settings

- **Templater** → Folder Templates → `Blog/drafts` → `post-template.md`
- **Files & Links** → Default attachment folder → `Blog/_images/${filename}`