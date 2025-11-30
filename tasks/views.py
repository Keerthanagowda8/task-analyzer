from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime

from tasks.models import Task 

def calculate_score(task):
    score = 0
    due_date = task.get('due_date')
    if due_date:
        try:
            due_obj = datetime.strptime(str(due_date), '%Y-%m-%d').date()
            days_until_due = (due_obj - datetime.now().date()).days
            
            if days_until_due < 0:
                overdue_days = abs(days_until_due)
                score += 35 + min(15, overdue_days) 
            elif days_until_due == 0:
                score += 35  
            elif days_until_due == 1:
                score += 30 
            elif days_until_due <= 3:
                score += 25  
            elif days_until_due <= 7:
                score += 18  
            elif days_until_due <= 14:
                score += 12  
            elif days_until_due <= 30:
                score += 6   
            else:
                score += 2   
        except Exception:
            score += 8  
    else:
        score += 8  

    importance = task.get('importance', 5)
    try:
        importance = max(1, min(10, int(importance)))
        if importance >= 9:
            score += 30
        elif importance >= 7:
            score += 24
        elif importance >= 5:
            score += 18
        elif importance >= 3:
            score += 12
        else:
            score += 6
    except Exception:
        score += 15  

    estimated_hours = task.get('estimated_hours')
    if estimated_hours is not None:
        try:
            hours = float(estimated_hours)
            if hours <= 0:
                score += 10  
            elif hours < 1:
                score += 20  
            elif hours <= 2:
                score += 16  
            elif hours <= 4:
                score += 12  
            elif hours <= 8:
                score += 8  
            else:
                score += 4   
        except Exception:
            score += 10
    else:
        score += 10  

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