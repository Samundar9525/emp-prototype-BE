# Loading sample database in postgres
To initialize the database in postgres run the following command
- point to the database directory
- psql -U username -c "CREATE DATABASE employee"
- psql -U username employee < employee.sql
  
Provide the password of your postgres the ERD diagram is shown below with (including django migrated tables)

![ERD](https://github.com/Samundar9525/emp-prototype-BE/assets/71628177/263539cc-5689-4917-8792-93cf9ba1983b)
