from PIL import Image

# Load the PGM file
pgm_image = Image.open('rac_lab/docmap (copy).pgm')

# Save the image as a PNG file
pgm_image.save('map.png')

print("Conversion complete: 'map.pgm' has been converted to 'map.png'")
