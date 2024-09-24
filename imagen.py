from PIL import Image
import numpy as np

def load_image(path):
    try:
        img = Image.open(path)
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def to_grayscale(img):
    return img.convert("L")

def resize_image(img, new_width=100):
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    resized_image = img.resize((new_width, new_height))
    return resized_image

def map_pixels_to_ascii(img, ascii_chars):
    pixels = np.array(img)
    ascii_image = []
    for pixel_row in pixels:
        ascii_row = "".join([ascii_chars[pixel // 25] for pixel in pixel_row])
        ascii_image.append(ascii_row)
    return "\n".join(ascii_image)

def create_ascii_art(image_path, new_width=100):
    ascii_chars = "@%#*+=-:. "  # From darkest to lightest
    img = load_image(image_path)
    if img is None:
        return
    
    grayscale_img = to_grayscale(img)
    resized_img = resize_image(grayscale_img, new_width)
    ascii_art = map_pixels_to_ascii(resized_img, ascii_chars)
    
    print(ascii_art)

if __name__ == "__main__":
    image_path = input("Enter the path to your image: ")
    create_ascii_art(image_path)
