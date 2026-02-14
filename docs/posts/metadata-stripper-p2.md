---
tags:
  - Python
  - Refactoring
  - TypeHinting
---
# Project: Exif-Eraser (Part 2) - Fighting the Linter

Building a tool isn't just about the logic; it's about making the code maintainable and "clean" for modern IDEs.

## The Type-Hinting Trap

While building the core stripping logic, I ran into a persistent error from **Pylance**:
> `Argument of type "ImagingCore" cannot be assigned to parameter "iterable"`

This happened because I was trying to manually iterate over pixels using `list(img.getdata())`. While this works in older Python scripts, modern linters struggle with Pillow's internal C-optimized objects.

## The Solution: img.copy()

Instead of rebuilding the image pixel-by-pixel, I refactored the code to use Pillow's native `copy()` method.

**Old Code (Buggy):**

```python
data = list(img.getdata())
clean_img = Image.new(img.mode, img.size)
clean_img.putdata(data)
```

### What I added (The Fix)

```python
with Image.open(file_path) as img:
    clean_img = img.copy() # Keeps pixels, drops the pointer to metadata
    clean_img.save(clean_path, exif=bytes()) # Nukes the EXIF block
```

This approach is faster, uses less memory, and—most importantly—satisfied the linter.
