import base64
import os

# Allowed image extensions
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")

# Loop through all files in the current directory
for filename in os.listdir('.'):
    # Skip non-image files
    if not filename.lower().endswith(IMAGE_EXTENSIONS):
        continue

    filepath = os.path.join('.', filename)

    try:
        # Open the image and encode in Base64
        with open(filepath, "rb") as img_file:
            b64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Build the output filename (same base name, .txt extension)
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}.txt"

        # Write the Base64 string to a text file
        with open(output_filename, "w", encoding="utf-8") as out_file:
            out_file.write(f"data:image/png;base64,{b64}")

        print(f"✅ Created {output_filename}")

    except Exception as e:
        print(f"⚠️ Skipped {filename}: {e}")
