from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Path to the certificate template
TEMPLATE_PATH = 'static/certificate_template.png'
FONT_PATH = 'static/Arial.ttf'

# Create certificates directory if it doesn't exist
if not os.path.exists('certificates'):
    os.makedirs('certificates')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_certificate():
    # Get form data (for POST requests)
    name = request.form['name']
    date = request.form['date']

    # Load the certificate template
    template = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(template)

    # Try to use a specific font, fallback to default if unavailable
    try:
        font_large = ImageFont.truetype(FONT_PATH, 50)  # Adjust font size
        font_medium = ImageFont.truetype(FONT_PATH, 20)  # Adjust font size
    except Exception:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()

    # Coordinates for text placement (adjust based on your template)
    name_coords = (490, 330)  # Adjusted X, Y for name based on your image
    date_coords = (280, 610)  # Adjusted X, Y for date based on your image

    # Add text to the template
    draw.text(name_coords, name, font=font_large, fill="white")
    draw.text(date_coords, date, font=font_medium, fill="white")

    # Save the certificate
    file_name = f"certificates/{name.replace(' ', '_')}_certificate.png"
    template.save(file_name)

    # Send the generated certificate to the user
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
