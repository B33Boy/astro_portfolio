import os
import re
import shutil
import sys
from pathlib import Path

import boto3
from dotenv import load_dotenv

# Load .env
load_dotenv(".env")

ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
PUBLIC_URL = os.getenv("R2_PUBLIC_URL").rstrip("/")

OBSIDIAN_PUBLISHED = Path(os.getenv("OBSIDIAN_PUBLISHED_PATH"))
OBSIDIAN_IMAGES = Path(os.getenv("OBSIDIAN_IMAGES_PATH"))
ASTRO_POSTS = Path(os.getenv("ASTRO_POSTS_PATH"))

# R2 client
s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name="auto",
)


def upload_image(local_path: Path, post_slug: str) -> str:
    """Upload an image to R2 and return its public URL."""
    r2_key = f"{post_slug}/{local_path.name}"
    print(f"  Uploading {local_path.name} → {r2_key}")
    s3.upload_file(
        str(local_path),
        BUCKET_NAME,
        r2_key,
        ExtraArgs={"ContentType": get_content_type(local_path)},
    )
    return f"{PUBLIC_URL}/{r2_key}"


def get_content_type(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(ext, "application/octet-stream")


def process_post(post_slug: str):
    source_file = OBSIDIAN_PUBLISHED / f"{post_slug}.md"
    images_dir = OBSIDIAN_IMAGES / post_slug
    dest_file = ASTRO_POSTS / f"{post_slug}.mdx"

    # Validate
    if not source_file.exists():
        print(f"Error: could not find {source_file}")
        sys.exit(1)

    content = source_file.read_text(encoding="utf-8")

    # Find all Obsidian-style image links: ![[image.png]]
    obsidian_links = re.findall(r"!\[\[(.+?)\]\]", content)

    if not obsidian_links:
        print("No Obsidian image links found, copying as-is.")
    else:
        print(f"Found {len(obsidian_links)} image(s) to upload:")

        for image_name in obsidian_links:
            local_image = images_dir / image_name

            if not local_image.exists():
                print(
                    f"  Warning: image not found at {local_image}, skipping.")
                continue

            r2_url = upload_image(local_image, post_slug)

            # Rewrite ![[image.png]] → ![image](https://...)
            content = content.replace(
                f"![[{image_name}]]",
                f"![{Path(image_name).stem}]({r2_url})",
            )

    # Write to Astro posts
    ASTRO_POSTS.mkdir(parents=True, exist_ok=True)
    dest_file.write_text(content, encoding="utf-8")
    print(f"\nPublished → {dest_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/publish.py <post-slug>")
        print("Example: python3 scripts/publish.py my-post-title")
        sys.exit(1)

    process_post(sys.argv[1])
