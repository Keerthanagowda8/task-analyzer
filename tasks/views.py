from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def calculate_score(task):
    score = 0
    importance = task.get('importance', 5)
    score += (importance * 5)
    hours = task.get('estimated_hours', 1)
    if hours < 2:
        score += 20
        
    return score

@csrf_exempt
def analyze_tasks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for task in data:
            task['score'] = calculate_score(task)
        sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)
        return JsonResponse(sorted_data, safe=False)    
    return JsonResponse({'error': 'Only POST allowed'}, status=400)