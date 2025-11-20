# app.py
from flask import Flask, request, jsonify, render_template_string
from azure.storage.blob import BlobServiceClient, ContentSettings
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env
load_dotenv()
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
IMAGES_CONTAINER = os.getenv("IMAGES_CONTAINER", "images-demo")

# Initialize Azure Blob client
bsc = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
images_cc = bsc.get_container_client(IMAGES_CONTAINER)

# Initialize Flask app
app = Flask(__name__)

# -----------------------------
# Home route
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return "Meme Generator API is running! Use /upload to upload images."

# -----------------------------
# HTML upload page for browser
# -----------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    html = """
    <h1>Meme Generator</h1>
    <form method="POST" enctype="multipart/form-data">
        Image: <input type="file" name="image"><br><br>
        Text: <input type="text" name="text"><br><br>
        <input type="submit" value="Upload Meme">
    </form>
    """
    if request.method == "POST":
        file = request.files.get("image")
        text = request.form.get("text")
        if not file or not text:
            return "Please provide both image and text."
        # Generate meme and upload
        url = create_meme(file, text)
        return f"Meme uploaded! <a href='{url}' target='_blank'>View Meme</a>"
    return render_template_string(html)

# -----------------------------
# API route for programmatic upload
# -----------------------------
@app.route("/upload-meme", methods=["POST"])
def upload_meme():
    file = request.files.get("image")
    text = request.form.get("text")
    if not file or not text:
        return jsonify({"error": "Missing image or text"}), 400

    url = create_meme(file, text)
    return jsonify({"meme_url": url})

# -----------------------------
# Function to create meme and upload to Azure Blob
# -----------------------------
def create_meme(file, text):
    # Open image with PIL
    img = Image.open(file)
    draw = ImageDraw.Draw(img)

    # Font: try Arial, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", size=40)
    except:
        font = ImageFont.load_default()

    # Draw text at top-left
    draw.text((10, 10), text, fill="white", font=font)

    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    # Unique blob name
    blob_name = f"meme-{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.jpg"
    blob_client = images_cc.get_blob_client(blob_name)

    # Upload to Azure Blob
    blob_client.upload_blob(
        img_bytes,
        overwrite=True,
        content_settings=ContentSettings(content_type="image/jpeg")
    )

    # Return public URL
    return blob_client.url

# -----------------------------
# Run Flask app
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

