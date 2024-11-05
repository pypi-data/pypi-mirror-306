from flask import Flask, jsonify, request, redirect
import os
import random
import boto3

app = Flask(__name__)

B2_ENDPOINT = 'https://s3.us-east-005.backblazeb2.com'  # Update if necessary
B2_BUCKET_NAME = 'prognosic-data-api'

B2_ACCESS_KEY = os.getenv('B2_ACCESS_KEY')  
B2_SECRET_KEY = os.getenv('B2_SECRET_KEY')  

# Initialize boto3 session and client for Backblaze B2
session = boto3.session.Session()
s3_client = session.client(
    's3',
    endpoint_url=B2_ENDPOINT,
    aws_access_key_id=B2_ACCESS_KEY,
    aws_secret_access_key=B2_SECRET_KEY
)

# Define cloud directories (these are subfolders in the bucket)
IMAGE_DIRS = {
    "normal_lung_ct": "images/normal_lung_ct",
    "lung_cancer_ct": "images/lung_cancer_ct",
}

@app.route('/get_images', methods=['GET'])
def get_images():
    # Get the category and number of images requested
    category = request.args.get('category')
    num_images = request.args.get('num', default=1, type=int)

    # Validate the category
    if category not in IMAGE_DIRS:
        return jsonify({"error": "Invalid category"}), 400

    # List all objects in the specified directory
    directory = IMAGE_DIRS[category]
    try:
        response = s3_client.list_objects_v2(Bucket=B2_BUCKET_NAME, Prefix=directory)
        all_images = [obj['Key'] for obj in response.get('Contents', [])
                      if obj['Key'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    except Exception as e:
        return jsonify({"error": f"Error accessing cloud storage: {str(e)}"}), 500

    # Randomly select the requested number of images
    selected_images = random.sample(all_images, min(num_images, len(all_images)))

    # Generate URLs for the selected images
    image_urls = [
        f"{B2_ENDPOINT}/{B2_BUCKET_NAME}/{img_key}" for img_key in selected_images
    ]

    return jsonify({"images": image_urls})

@app.route('/download_image/<category>/<image_name>', methods=['GET'])
def download_image(category, image_name):
    # Validate the category
    if category not in IMAGE_DIRS:
        return jsonify({"error": "Invalid category"}), 400

    # Form the cloud path for the image
    image_path = f"{IMAGE_DIRS[category]}/{image_name}"

    # Generate a pre-signed URL for the image
    try:
        image_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': B2_BUCKET_NAME, 'Key': image_path},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return redirect(image_url)
    except Exception as e:
        return jsonify({"error": f"Could not generate URL: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
