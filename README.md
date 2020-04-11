# DjangoPollApp
Django practice with tutorial, a poll application

notes
1. Database table migration
Migrations are very powerful and let you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones - it specializes in upgrading your database live, without losing data. We’ll cover them in more depth in a later part of the tutorial, but for now, remember the three-step guide to making model changes:

Change your models (in models.py).
Run "python manage.py makemigrations {appname}" to create migrations for those changes
Run "python manage.py migrate" to apply those changes to the database.

2. python3 manage.py shell