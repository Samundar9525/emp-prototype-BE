from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('view_employee', '0005_create_employee_department_view'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE OR REPLACE VIEW department_employee_counts AS
            SELECT 
                d.dept_no,
                d.dept_name,
                COUNT(de.emp_no) as total_employees
            FROM 
                department d
                LEFT JOIN dept_emp de ON d.dept_no = de.dept_no
                AND de.to_date >= CURRENT_DATE
            GROUP BY 
                d.dept_no, d.dept_name;
        """,
        "DROP VIEW IF EXISTS department_employee_counts;")
    ]
