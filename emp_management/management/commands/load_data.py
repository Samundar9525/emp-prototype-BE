from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Load data from SQL files'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        dataset_dir = os.path.join(base_dir, 'dataset_large')
        
        sql_files = [
            'load_department.sql',
            'load_employee.sql',
            'load_dept_emp.sql',
            'load_dept_manager.sql',
            'load_salary1.sql',
            'load_title.sql',
        ]
        
        with connection.cursor() as cursor:
            for sql_file in sql_files:
                file_path = os.path.join(dataset_dir, sql_file)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        sql = f.read()
                    cursor.execute(sql)
                    self.stdout.write(f'Successfully loaded {sql_file}')
                else:
                    self.stdout.write(f'File {sql_file} not found')