from django.test import TestCase
from datetime import date, timedelta
from tasks.views import calculate_score

class TaskScoreTests(TestCase):
    def setUp(self):
        
        self.today = date.today()
        
    def test_urgency_scoring(self):
        """Test how due dates affect the score"""
        
        # 1. Overdue Task (5 days ago)
        # Logic: 35 + min(15, 5) = 40 points
        overdue_task = {
            'due_date': str(self.today - timedelta(days=5)),
            'importance': 1, 'estimated_hours': 100 # minimal points for others
        }
        # Expected: 40 (urgency) + 6 (imp < 3) + 4 (effort > 8) = 50
        self.assertEqual(calculate_score(overdue_task), 50, "Overdue task score incorrect")

        # 2. Due Today
        # Logic: 35 points
        today_task = {
            'due_date': str(self.today),
            'importance': 1, 'estimated_hours': 100
        }
        # Expected: 35 + 6 + 4 = 45
        self.assertEqual(calculate_score(today_task), 45, "Due today score incorrect")

        # 3. Due Tomorrow
        # Logic: 30 points
        tomorrow_task = {
            'due_date': str(self.today + timedelta(days=1)),
            'importance': 1, 'estimated_hours': 100
        }
        # Expected: 30 + 6 + 4 = 40
        self.assertEqual(calculate_score(tomorrow_task), 40, "Due tomorrow score incorrect")

        # 4. Due in 7 days (This week)
        # Logic: 18 points
        week_task = {
            'due_date': str(self.today + timedelta(days=7)),
            'importance': 1, 'estimated_hours': 100
        }
        # Expected: 18 + 6 + 4 = 28
        self.assertEqual(calculate_score(week_task), 28, "Due this week score incorrect")

    def test_importance_scoring(self):
        """Test how importance ratings affect the score"""
        base_task = {
            'due_date': None, # +8 points
            'estimated_hours': 100 # +4 points
        }
        # Base score without importance = 12

        # Importance 9 (High) -> +30
        task_high = base_task.copy()
        task_high['importance'] = 9
        self.assertEqual(calculate_score(task_high), 12 + 30)

        # Importance 7 (Medium-High) -> +24
        task_med_high = base_task.copy()
        task_med_high['importance'] = 7
        self.assertEqual(calculate_score(task_med_high), 12 + 24)

        # Importance 5 (Medium) -> +18
        task_med = base_task.copy()
        task_med['importance'] = 5
        self.assertEqual(calculate_score(task_med), 12 + 18)

        # Importance 1 (Low) -> +6
        task_low = base_task.copy()
        task_low['importance'] = 1
        self.assertEqual(calculate_score(task_low), 12 + 6)

    def test_effort_scoring(self):
        """Test how estimated effort (Quick wins) affects the score"""
        base_task = {
            'due_date': None, # +8
            'importance': 1   # +6
        }
        # Base score without effort = 14

        # < 1 hour (Quick win) -> +20
        task_quick = base_task.copy()
        task_quick['estimated_hours'] = 0.5
        self.assertEqual(calculate_score(task_quick), 14 + 20)

        # 2 hours -> +16
        task_short = base_task.copy()
        task_short['estimated_hours'] = 2
        self.assertEqual(calculate_score(task_short), 14 + 16)

        # 4 hours -> +12
        task_medium = base_task.copy()
        task_medium['estimated_hours'] = 4
        self.assertEqual(calculate_score(task_medium), 14 + 12)

        # 10 hours (Long task) -> +4
        task_long = base_task.copy()
        task_long['estimated_hours'] = 10
        self.assertEqual(calculate_score(task_long), 14 + 4)

    def test_edge_cases(self):
        """Test missing data or invalid inputs"""
        
        # Missing date, importance, and hours
        # Urgency: None -> +8
        # Importance: None (defaults to 15 in exception/default logic? Let's check logic)
        # Your code: importance.get defaults to 5. 
        # Logic: 5 -> +18
        # Effort: None -> +10
        empty_task = {} 
        # Expected: 8 + 18 + 10 = 36
        self.assertEqual(calculate_score(empty_task), 36)

        bad_date_task = {'due_date': 'not-a-date', 'importance': 1, 'estimated_hours': 10}
        self.assertEqual(calculate_score(bad_date_task), 18)