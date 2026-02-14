---
tags:
  - Python
  - Forensics
  - Privacy
---
# Project: Exif-Eraser (Part 1) - The Hidden Payload

When you upload a photo to this blog, you aren't just uploading pixels. You're uploading a digital fingerprint.

## The Forensic Problem

Every JPEG contains a header called **EXIF (Exchangeable Image File Format)**. In a typical photo, this header reveals:

* **GPS Coordinates**: Where the photo was taken (latitude/longitude).
* **Device Identity**: Your camera model and serial number.
* **Software**: The exact version of the editor you used.

## The Goal

Build a Python tool that recursively "nukes" this metadata block while keeping the image quality at 100%.

## The "Dry Run" Philosophy

A professional forensic tool shouldn't be a "black box." My first step was implementing a **Dry Run** mode. This allows me to audit my `docs/assets` folder to see exactly what hidden data is lurking in my project before I commit to a sweep.

> **Next Up**: In Part 2, I'll deep-dive into the `Pillow` logic and how I solved the `ImagingCore` type-hinting issues.
