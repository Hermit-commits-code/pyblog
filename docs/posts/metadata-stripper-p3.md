---
tags:
  - Python
  - Automation
  - Security
---
# Project: Exif-Eraser (Part 3) - The Full Implementation

In this final installment, we move from a single-file script to a recursive CLI tool capable of auditing and cleaning entire project directories.

## Recursive Directory Walking

Using Python's `os.walk`, we can traverse deep into folder structures to find assets. A critical part of this logic was ensuring we didn't get caught in an infinite loop or accidentally re-process files we've already cleaned.

### The Implementation Logic

We used a naming convention filter `_clean` to identify files that have already been sanitized.

```python
# snippet of our recursive filter
if file.lower().endswith(valid_exts) and "_clean" not in file:
    full_path = os.path.join(root, file)
    strip_image_metadata(full_path, dry_run=dry_run)
```

### The Safety Protocol: Dry Run

As discussed in Part 1, forensic tools must be non-destructive by default. My implementation defaults to dry_run=True, which simply logs the files to the terminal without touching the disk.

This allowed me to audit my ./docs/assets folder and discover exactly which screenshots were leaking system data before performing a bulk sanitize.
Conclusion

The Exif-Eraser is now a permanent part of my deployment pipeline. Every image uploaded to this blog now passes through this filter, ensuring that my privacy—and my GPS coordinates—remain private.
