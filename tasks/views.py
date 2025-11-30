from django.shortcuts import render
import json
from django.http import JsonResponse

def analyze_tasks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Only POST allowed'}, status=400)