import uuid
from .tasks import process_csv_file
from .models import RequestStatus
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from django.http import JsonResponse

@api_view(['POST'])
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        file_path = default_storage.save(f"uploads/{csv_file.name}", csv_file)
        request_id = str(uuid.uuid4())
        
        # Create initial request status
        RequestStatus.objects.create(request_id=request_id, status='waiting')
        
        # Call the process_csv_file task
        process_csv_file.delay(file_path, request_id)
        
        return JsonResponse({'request_id': request_id, 'status': 'In queue'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['GET'])
def check_request_status(request, request_id):
    try:
        request_status = RequestStatus.objects.get(request_id=request_id)
        return JsonResponse({
            'request_id': request_status.request_id,
            'status': request_status.status,
            'result': request_status.result
        })
    except RequestStatus.DoesNotExist:
        return JsonResponse({'error': 'Request ID not found'}, status=404)