from PIL import Image

# Open the grayscale image
gray_image = Image.open("gray_image.png")

# Define the color you want to shade the image with
shade_color = (255, 127, 63, 255)  # Red color, you can change this to any other color
trans_color = (255, 0, 254, 255)  # Transparent color

# Convert the grayscale image to RGBA format
rgba_image = gray_image.convert("RGBA")

# Create a new RGBA image of the same size as the grayscale image
shaded_image = Image.new("RGBA", rgba_image.size)

# Iterate over each pixel of the grayscale image and apply the shade color
for x in range(rgba_image.width):
    for y in range(rgba_image.height):
        pixel = rgba_image.getpixel((x, y))
        if pixel == trans_color:
            shaded_pixel = (0, 0, 0, 0)
        else:
            intensity = pixel[0]  # Grayscale intensity
            shaded_pixel = (shade_color[0], shade_color[1], shade_color[2], intensity)
        shaded_image.putpixel((x, y), shaded_pixel)

# Display or save the resulting shaded image
shaded_image.show()  # Display the shaded image
shaded_image.save("shaded_image.png")  # Save the shaded image
