from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('view_employee', '0010_alter_salary_emp_no_alter_salary_from_date'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW designation_timeline AS
            SELECT 
                t.emp_no as employee_id,
                t.title,
                t.from_date,
                EXTRACT(YEAR FROM age(COALESCE(t.to_date, CURRENT_DATE), t.from_date)) as years
            FROM 
                title t
            ORDER BY 
                t.emp_no, t.from_date;
            """,
            "DROP VIEW IF EXISTS designation_timeline;"
        ),
    ]
