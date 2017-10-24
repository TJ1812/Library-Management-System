Requirements(Recommended)
1)	Windows 10
2)	Google Chrome
3)	Python 3.5
4)	MySQL 5.7 – All Packages (Server, Client)
5)	Pymysql (pip install pymysql)
6)	Mysqlclient or MYSQL-python (pip install mysqlclient)
7)	Pandas (pip install pandas)
8)	Django (pip install Django)

-First make sure that MySQL service is running by going to mysql command line tool.
-If it is not running go to start->run and type 'services.msc' and locate mysql 5.7 server and start it.
-After fulfilling all requirements, extract the zip file.
-After extracting, open console and go to location of extracted folder.
-Run python createTables.py to create database.
-Run python initializeTables.py to populate the database.
-After that type go to Library Management System folder where manage.py file is there.
-Type, python manage.py makemigrations
-Type, python manage.py migrate
-Type, python manage.py createsuperuser, to create a superuser. Enter user name and password.
-To run server, type, python manage.py runserver
-After that go to google chrome and type 127.0.0.1:8000 and start using the app and make sure you are connected to internet.
