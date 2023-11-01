import json
import os
from django.db import Error
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FileData, FolderData


@csrf_exempt
def store_pd(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)

        pk_name_location = f"{received_data.get('name', '')}_{received_data.get('location', '')}"
        if not FileData.objects.filter(pk_name_location=pk_name_location).exists():
            file_data = FileData(
                name=received_data.get('name', ''),
                content=received_data.get('content', ''),
                location=received_data.get('location', ''),
                pk_name_location=pk_name_location
            )
            file_data.save()
            return JsonResponse({'message': 'Data received and stored successfully'}, status=201)
        else:
            return JsonResponse({'message': 'File already exists in the storage'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def retrieve_pd(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body.decode('utf-8'))

            directory = received_data.get('directory', '')
            print(received_data, type(received_data), 'data')
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)

        if directory and os.path.exists(directory) and os.path.isdir(directory):

            matching_records = FileData.objects.filter(location=directory)

            files_in_directory = [record.name for record in matching_records]
            return JsonResponse({'files': files_in_directory})
        else:
            return JsonResponse({'error': 'Invalid directory path or directory does not exist'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def retrieveFile(request):
    if request.method == 'POST':
        name = ''
        location = ''
        try:
            received_data = json.loads(request.body.decode('utf-8'))
            name = received_data.get('name', '')
            location = received_data.get('location', '')
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)

        pk_name_location = f"{name}_{location}"

        try:
            file_data = FileData.objects.get(pk_name_location=pk_name_location)

            response = HttpResponse(
                file_data.content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{name}"'
            return response
        except FileData.DoesNotExist:
            return JsonResponse({'error': 'File not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def search(request):
    if request.method == 'POST':
        name = ''
        try:
            received_data = json.loads(request.body.decode('utf-8'))
            name = received_data.get('name', '')
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)

        try:
            matching_records = FileData.objects.filter(name=name)
            files_data = []

            for record in matching_records:
                file_info = {
                    'name': record.name,
                    'timestamp': record.timestamp,
                    'location': record.location,
                }
                files_data.append(file_info)

            return JsonResponse({'files': files_data})
        except FileData.DoesNotExist:
            return JsonResponse({'error': 'File not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def storeFolder(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body.decode('utf-8'))
            print(received_data, 'received_data')
            name = received_data.get('name', '')
            location = received_data.get('address', '')
            num_files = received_data.get('numFiles', 0)
            files = received_data.get('files', [])
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)

        folder_key = f"{name}_{location}"
        print(folder_key, 'folder_key', name, location, num_files, files)
        try:
            existing_folder = None
            try:
                FolderData.objects.filter(pk=folder_key).first()
            except:
                pass
            if existing_folder:
                print('folder already exists')
                return JsonResponse({'message': 'Folder already exists.'}, status=200)
            else:
                print('not exist')
                folder_data = FolderData(
                    name=name,
                    location=location,
                    num_files=num_files,
                )
                folder_data.save()
                print('files in fodler', files)
                # Save associated files
                for file_info in files:
                    file = FileData(
                        name=file_info['name'],
                        content=file_info.get('content', ''),
                        location=location,
                    )
                    file.save()
                    folder_data.files.add(file)
                print('folder saved')
                return JsonResponse({'message': 'Folder received and stored successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'Error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)