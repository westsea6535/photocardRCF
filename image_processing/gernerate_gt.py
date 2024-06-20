from PIL import Image

image_name = "246668094_1_1715241595_w_2px.png"
image_path = f"./imagesWithEdge/{image_name}"

# Open the PNG file
image = Image.open(image_path)

# Get the pixel values
pixels = list(image.getdata())

# Print the pixel values
for i in range(len(pixels)):
    if pixels[i][3] == 0:
        pixels[i] = (0, 0, 0, 255)


# Save the modified pixel values back to the image
image.putdata(pixels)

# Save the image
image.save(image_path)