from PIL import Image, ImageDraw, ImageFont,ImageFilter
import random
import os

def gen_txt2img(index, content, font_size=30, font_color="black", font_path="KhmerOScontent.ttf",
                background_image_path=None, noise_level=0.05, opacity=255, blur_level=0,
                noise_type='gaussian', output_format="png", padding=2):

    current_path = os.getcwd()
    output_path = os.path.join(current_path, "output")
    os.makedirs(output_path, exist_ok=True)

    # Load the font, using a default one if the specified font is not available
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found. Please make sure you have the Khmer font installed.")
        font = ImageFont.load_default()

    # Create a temporary image to calculate text size
    temp_image = Image.new('RGBA', (1, 1), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(temp_image)
    bbox = draw.textbbox((0, 0), content, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Adjust the background image size to fit the text with padding
    image_width = text_width + 2 * padding
    image_height = text_height + 2 * padding

    # Load the background image or create a plain background if not provided
    if background_image_path and os.path.isfile(background_image_path):
        bg_image = Image.open(background_image_path).convert("RGBA")
        bg_image = bg_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
    else:
        # Default background if no image is provided
        bg_image = Image.new('RGBA', (image_width, image_height), color=(255, 255, 255, 255))  # White background

    # Create an image for the text with transparency
    text_image = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0, 0), content, font=font, fill=(0, 0, 0, opacity))

    # Center the text image onto the background image
    x = (bg_image.width - text_image.width) // 2
    y = (bg_image.height - text_image.height) // 2
    bg_image.paste(text_image, (x, y), text_image)

    # Generate noise based on the specified type
    if noise_level > 0:
        noise = Image.effect_noise((bg_image.width, bg_image.height), int(noise_level * 100))
        noise = noise.convert("RGBA")

        if noise_type == 'gaussian':
            noise = noise.point(lambda i: i * random.uniform(0.5, 1.5))
        elif noise_type == 'salt_pepper':
            noise = noise.point(lambda i: 0 if random.random() < 0.5 else 255)

        # Blend the noise with the background image
        bg_image = Image.blend(bg_image, noise, alpha=0.2)

    # Apply blur effect if specified
    if blur_level > 0:
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(blur_level))

    # Save the final image to a file
    output_file = os.path.join(output_path, f"{index}.{output_format}")
    bg_image = bg_image.convert("RGB")  # Convert to RGB before saving to handle non-transparent formats
    bg_image.save(output_file, format=output_format.upper())

    print(f"Image saved at: {output_file}")

def gen_txt2img2(index, content, font_size=30,font_color="black",font_path="KhmerOScontent.ttf"):
    
    current_path = os.getcwd()
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found. Please make sure you have the Khmer font installed.")
        font = ImageFont.load_default()
    temp_image = Image.new('RGB', (1, 1), color='white')
    draw = ImageDraw.Draw(temp_image)

    bbox = draw.textbbox((0, 0), content, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Add some padding around the text
    image = Image.new('RGB', (text_width + 4, text_height + 4), color='white') 
    draw = ImageDraw.Draw(image)
    
    position = (2, 2)
    draw.text(position, content, fill=font_color, font=font)

    # Save the image to a file
    full_path = os.path.join(current_path,"output",str(index)+".jpg")
    image.save(full_path)