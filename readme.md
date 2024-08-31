# Image Processing API

This project provides an API to process CSV files containing image URLs. The API downloads and compresses the images, stores the compressed images in a specified folder, and updates the CSV file with the URLs of the compressed images.

## Setup

### Prerequisites

- Python 3.6+
- Django 3.0+
- Celery 4.0+
- Redis (for Celery broker)
- Pillow (Python Imaging Library)

### Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/image-processing-api.git
   cd image-processing-api
   ```
2. **Create a virtual environment**:

    ```sh
    python3 -m venv env
    ```

3. **Activate the virtual environment**:

    ```sh
    source env/bin/activate
    ```

4. **Install the required packages**:

    ```sh
    pip install -r requirements.txt
    ```

5. **Start the Redis server**:

    ```sh
    redis-server
    ```

6. **Start Celery worker**:

    ```sh
    celery -A your_project_name worker --loglevel=info
    ```

7. **Start the Django development server**:

    ```sh
    python manage.py runserver
    ```



## Usage

### Uploading CSV File

To process a CSV file containing image URLs, make a POST request to the following endpoint:

```
http://127.0.0.1:8000/imagi-process/upload_csv/
```

Include the CSV file as the payload of the request. The API will asynchronously process the images and store the compressed versions in the specified folder.

### Checking Request Status

To check the status of a processing request, use the following endpoint:

```
http://127.0.0.1:8000/imagi-process/check_request_status/31a822c9-de10-48d7-970b-28159fdd741a/
```

Replace `31a822c9-de10-48d7-970b-28159fdd741a` with the actual request ID. This API endpoint will provide information about the progress and status of the request.

Please note that the processing of images is done asynchronously, so it may take some time before the request status is updated.

## Testing

### Uploading CSV File

To test the API's ability to process a CSV file containing image URLs, you can use the `curl` command to make a POST request. Replace `/path/to/csv/file.csv` with the actual path to your CSV file.

```sh
curl --location 'http://127.0.0.1:8000/imagi-process/upload_csv/' \
--form 'file=@"/path/to/csv/file.csv"'
```


This command will send the CSV file as the payload of the request to the specified endpoint. The API will asynchronously process the images and store the compressed versions in the specified folder.

### Sample response
```sh
{
    "request_id": "bd158f56-81ca-4591-9e7a-925fe9314af4",
    "status": "In queue"
}
```

### Checking Request Status

To test the API's ability to check the status of a processing request, you can use the `curl` command to make a GET request. Replace `request_id` with the actual request ID.

```sh
curl --location 'http://127.0.0.1:8000/imagi-process/check_request_status/request_id/'
```

### Sample response

```sh
{
    "request_id": "31a822c9-de10-48d7-970b-28159fdd741a",
    "status": "completed",
    "result": "uploads/products_ebIcRGw.csv"
}
```
