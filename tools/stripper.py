import os

from PIL import Image


def strip_image_metadata(file_path, dry_run=False):
    """Opens an image, removes EXIF data, and saves it."""
    if dry_run:
        print(f"[DRY RUN] Would sanitize: {file_path}")
        return

    with Image.open(file_path) as img:
        # This effectively creates a new image with only pixel data.
        clean_img = img.copy()
        # Generate a new filename
        base, ext = os.path.splitext(file_path)
        clean_path = f"{base}_clean{ext}"

        # Nukes the metablock
        clean_img.save(clean_path, exif=bytes())

    print(f"[✔] Sanitized: {clean_path}")


def process_all_images(root_dir, dry_run=True):
    """Recursively finds and cleans images in the specified directory"""
    valid_exts = (".jpg", ".jpeg", ".png")

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(valid_exts) and "_clean" not in file:
                full_path = os.path.join(root, file)
                strip_image_metadata(full_path, dry_run=dry_run)


if __name__ == "__main__":
    # Define the target: your blog's image folder
    target_folder = "./docs/assets"

    print(f"--- Starting Metadata Audit on {target_folder} ---")

    # Set dry_run=True to audit, False to actually clean
    process_all_images(target_folder, dry_run=False)

    print("--- Audit Complete ---")
