from PIL import Image
import requests
from io import BytesIO
from django.core.files.base import ContentFile
import csv
from celery import shared_task
from django.core.files.storage import default_storage
import logging
from .models import RequestStatus
import os

logger = logging.getLogger(__name__)

def process_csv_row(row, request_id):
    output_urls = []
    for image_url in row['input_urls'].split(','):
        image_url = image_url.strip()
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            error_message = f'Failed to download image from {image_url}: {e}'
            logger.error(error_message)
            result = {'request_id': request_id, 'status': 'error', 'error': error_message}
            RequestStatus.objects.filter(request_id=request_id).update(status='error', result=result)
            return result
        
        # Compress the image by 50%
        try:
            output_io = BytesIO()
            image_format = image.format if image.format else 'JPEG'
            image = image.resize((image.width // 2, image.height // 2), Image.LANCZOS)
            image.save(output_io, format=image_format)

            # Define the folder path
            folder_path = 'compressed_images'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            # Save the compressed image to storage
            compressed_image_name = f"{folder_path}/compressed_{os.path.basename(image_url)}.{image_format.lower()}"
            compressed_image_path = default_storage.save(compressed_image_name, ContentFile(output_io.getvalue()))
            compressed_image_url = default_storage.url(compressed_image_path)
            
            output_urls.append(compressed_image_url)
        except Exception as e:
            error_message = f'Failed to compress image from {image_url}: {e}'
            logger.error(error_message)
            result = {'request_id': request_id, 'status': 'error', 'error': error_message}
            RequestStatus.objects.filter(request_id=request_id).update(status='error', result=result)
            return result
    
    # Update the row with the output URLs
    row['output_urls'] = ','.join(output_urls)
    
    # Save the product data with compressed images
    product_data = {
        'serial_number': row['serial_number'],  # Ensure consistent key names
        'name': row['name'],
        'input_urls': row['input_urls'],
        'output_urls': ','.join(output_urls),  # Save as a single string of comma-separated URLs
    }

    RequestStatus.objects.filter(request_id=request_id).update(status='completed', result=product_data)
    result = {'request_id': request_id, 'status': 'success', 'data': product_data}

    return result

@shared_task
def process_csv_file(file_path, request_id):
    # Update status to inProgress
    RequestStatus.objects.filter(request_id=request_id).update(status='inProgress')
    
    updated_rows = []
    with default_storage.open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result = process_csv_row(row, request_id)
            if result['status'] == 'success':
                updated_rows.append(result['data'])
            else:
                logger.error(f"Failed to process row: {row} - {result['error']}")
    
    # Define the fieldnames to match the keys in the dictionary
    fieldnames = ['serial_number', 'name', 'input_urls', 'output_urls']
    
    # Write the updated rows to a new CSV file
    output_file_path = file_path
    with default_storage.open(output_file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in updated_rows:
            writer.writerow(row)
    
    # Update status to completed and store the file path
    RequestStatus.objects.filter(request_id=request_id).update(status='completed', result=output_file_path)
    
    return output_file_path