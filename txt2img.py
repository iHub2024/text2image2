from PIL import Image, ImageDraw, ImageFont

font_path = "KhmerOScontent.ttf"

khmer_text = "សួស្តី ប្រទេសកម្ពុជា! ប៊ីន សុភ័ក្ត្រា"  # This means "Hello, World!" in Khmer
font_size = 40

try:
    font = ImageFont.truetype(font_path, font_size)
except IOError:
    print("Font file not found. Please make sure you have the Khmer font installed.")
    font = ImageFont.load_default()
temp_image = Image.new('RGB', (1, 1), color='white')
draw = ImageDraw.Draw(temp_image)

bbox = draw.textbbox((0, 0), khmer_text, font=font)
text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

 # Add some padding around the text
image = Image.new('RGB', (text_width + 6, text_height + 6), color='white') 
draw = ImageDraw.Draw(image)

# Adding a fixed padding of 10 pixels
position = (3, 3)

draw.text(position, khmer_text, fill="black", font=font)

# Save the image to a file
image.save('khmer_text_image_cropped.png')

# Display the image
image.show()