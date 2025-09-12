from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('view_employee', '0004_departmentemployeecounts_employeedepartmentview_and_more'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE OR REPLACE VIEW employee_department_view AS
            SELECT 
                e.emp_no as employee_id,
                CONCAT(e.first_name, ' ', e.last_name) as employee_name,
                d.dept_no as department_id,
                d.dept_name as department_name,
                de.from_date,
                de.to_date
            FROM 
                employee e
                JOIN dept_emp de ON e.emp_no = de.emp_no
                JOIN department d ON de.dept_no = d.dept_no;
        """,
        "DROP VIEW IF EXISTS employee_department_view;")
    ]
