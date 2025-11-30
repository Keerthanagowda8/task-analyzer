from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime

from tasks.models import Task 

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

            saved_tasks = []
            for item in data:
                
                # add task to DB
                task_obj = Task.objects.create(
                    title=item.get('title', 'Untitled'),
                    due_date=item.get('due_date', date.today()), 
                    importance=item.get('importance', 5),
                    estimated_hours=item.get('estimated_hours', 1)
                )
                
                task_dict = {
                    'id': task_obj.id,
                    'title': task_obj.title,
                    'due_date': str(task_obj.due_date),
                    'importance': task_obj.importance,
                    'estimated_hours': task_obj.estimated_hours
                }
                
                task_dict['score'] = calculate_score(task_dict)
                saved_tasks.append(task_dict)

            print(saved_tasks) 
            
            sorted_data = sorted(saved_tasks, key=lambda x: x['score'], reverse=True)
            return JsonResponse(sorted_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'POST method required'}, status=405)