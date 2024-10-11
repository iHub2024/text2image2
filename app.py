from clsglobal import gen_txt2img

content = "សួស្តី ប្រទេសកម្ពុជា! ប៊ីន សុភ័ក្ត្រា"


gen_txt2img(index=1, content=content, font_size=40, font_color="black",
            background_image_path="background.jpg", noise_level=0.03, opacity=200, 
            blur_level=1, noise_type='salt_pepper', output_format="png")