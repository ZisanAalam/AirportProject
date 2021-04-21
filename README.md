<h1>Installation</h1>
<br>
<ol>
<li>Install the requirements after creating a virtual environment. </li>
<br>

```bash
pip install -r requirements.txt
```

<li>Create a <i>.env</i> file in the project directory and add the following information</li><br>

```
SECRET_KEY=Write_Project_Secret_Key_From_Settings.py
DATABASE_NAME=Write_Database_Name
DATABASE_HOST=Write_Database_host(usually localhost)
DATABASE_USER=Write_database_user(usually root)
DATABASE_PASSWORD=Write_database_password
```

<li> Makemigrations and then migrate the new model</li><br>

```bash
python manage.py makemigrations
python manage.py migrate
```

<li>Create a new instance of the Airport model. Each user should be connected with an airport. But since we do not want superuser to be connected to any airport, it would be preferable to have the name "None".</li><br>

```bash
python manage.py shell
```

```python
from account.models import Airport
a=Airport(name="None")
a.save()
a.id
```

<li>Take note of the id, and then create a superuser</li><br>

```bash
python manage.py createsuperuser
```

<li>Finally, go to the admin page and login with the superuser credentials. Create a group, you may call it Airport admin, and assign the permissions as you see fit. Do not allow Airport admin to add/change/view/delete new airport, but to give it permissions to manage users. Airport admin can be created by adding new airport and assigning that user to the airport along with giving the "is staff" permission and adding it to the aforementioned group.</li><br>
<li>Currently, when adding new normal users, the default value of "is active" is false. Meaning even after the users have been created they will not be able to login until they have been verified by the admins or the superuser.</li>
<br><br>
<hr>
