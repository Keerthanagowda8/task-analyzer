from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime 

def calculate_score(task):
    score = 0
    due_date_str = task.get('due_date') 
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            today = date.today()
            days_left = (due_date - today).days
            if days_left < 0:
                score += 100  
            elif days_left <= 3:
                score += 50   
            elif days_left <= 7:
                score += 20      
        except ValueError:
            pass
    importance = task.get('importance', 5)
    score += (importance * 5)
    hours = task.get('estimated_hours', 1)
    if hours < 2:
        score += 20   
    return score

@csrf_exempt
def analyze_tasks(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, dict): 
                data = [data]  
            for task in data:
                task['score'] = calculate_score(task)
            sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)
            return JsonResponse(sorted_data, safe=False)    
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Bad JSON Format'}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=400)