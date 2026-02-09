#!/usr/bin/env python3
"""Scan extracted frames for barcodes and QR codes."""
import sys
import os
import glob
from PIL import Image
from pyzbar.pyzbar import decode


def scan_directory(scan_dir):
    """Scan all images in a directory for barcodes/QR codes."""
    results = []
    image_files = sorted(
        glob.glob(f"{scan_dir}/*.jpg")
        + glob.glob(f"{scan_dir}/*.png")
        + glob.glob(f"{scan_dir}/*.jpeg")
    )

    print(f"Scanning {len(image_files)} images in {scan_dir}...")

    for img_path in image_files:
        try:
            img = Image.open(img_path)
            barcodes = decode(img)
            if barcodes:
                for bc in barcodes:
                    result = f"{os.path.basename(img_path)}: {bc.type} = {bc.data.decode()}"
                    results.append(result)
                    print(f"  FOUND: {result}")
        except Exception as e:
            print(f"  Error processing {img_path}: {e}")

    if not results:
        print("No barcodes or QR codes found.")
    else:
        output_file = os.path.join(scan_dir, "barcodes_found.txt")
        with open(output_file, "w") as f:
            f.write("\n".join(results))
        print(f"\n{len(results)} barcode(s) saved to {output_file}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scan_barcodes.py <directory_of_images>")
        sys.exit(1)

    scan_directory(sys.argv[1])
