from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
    max_index = len(ascii_chars) - 1

    for pixel_row in pixels:
        ascii_row = "".join([ascii_chars[min(pixel // 25, max_index)] for pixel in pixel_row])
        ascii_image.append(ascii_row)

    return "\n".join(ascii_image)

def create_ascii_art(image_path, new_width=100):
    ascii_chars = "@%#*+=-:. "  # From darkest to lightest
    img = Image.open(image_path)
    grayscale_img = to_grayscale(img)
    resized_img = resize_image(grayscale_img, new_width)
    ascii_art = map_pixels_to_ascii(resized_img, ascii_chars)
    return ascii_art

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        ascii_art = create_ascii_art(filepath)
        return render_template('result.html', ascii_art=ascii_art)

if __name__ == '__main__':
    app.run(debug=True)
