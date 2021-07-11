<h1>Installation</h1>
<br>
<ol>
  <li>Clone the repository using the following command.</li><br>
  
  ```bash
  git clone https://github.com/ZisanAalam/AirportProject.git
  ```
  
  <li>Setup a virtual environment. In this example, we use <i>virtualenv</i> , which is used to create isolated Python environments.</li>
  <i>virtualenv</i> can be installed using the following command.<br><br>
  
  ```bash
  pip install virtualenv
  ```
  
  Next, we create the virtual environment for our project. Change the current working directory to the directory where you cloned the project and enter the following command.
  <br>
  ```bash
  virtualenv AirportProject
  cd AirportProject/
  source bin/activate
  ```
  
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
</ol>
<h1>Deployment</h1>
<br>
The deployment procedures vary with different factors; one of them being the platform chosen. The procedure below shows the deployment procedures in a Linux machine(commands shown for Ubuntu, but packages are available for most distributions). We use <a href="https://www.nginx.com/">NGINX</a> web server, but since it doesn't support wsgi specifications, we need <a href="https://uwsgi-docs.readthedocs.io/en/latest/">uWSGI</a> as well. uWSGI in itself is a pretty capable http server but NGINX is preferred for its high throughput of static content.<br><br>
<ol>
  <li>First, in <i>settings.py</i>, change the following lines</li><br>
  
  ```python
  DEBUG=False
  #This is just a placeholder domain, change the domain to the one you've purchased.
  ALLOWED_HOSTS=['airportauthority.com.in', 'www.airportauthority.com.in']
  ```
  
<li>Install uWSGI package.</li><br>
  
```bash
pip install uwsgi
```
<i>It should be noted that the uwsgi requires python dev packages installed which can be done using the following command.</i><br>

```bash
  sudo apt-get install python3.8-dev
```
<li>Install the NGINX package and start the http server.</li><br>

```bash
  sudo apt-get install nginx
  sudo /etc/init.d/nginx start  
```
  <li>Create the nginx configuration files as follows.</li>
  You will need the uwsgi_params file, which is available <a href="https://github.com/nginx/nginx/blob/master/conf/uwsgi_params">here</a>. This should be copied into the project directory.
 Now create a file called AirportProject_nginx.conf in the /etc/nginx/sites-available/ directory, and add the following. Make sure to replace the paths and the DNS to match your specifications.
  
  ```conf
  # AirportProject_nginx.conf

# the upstream component nginx needs to connect to
upstream django {
    server unix:///path/to/cloned/repo/AirportProject/AirportProject.sock; # for a file socket
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name www.airportauthority.com.in airportauthority.com.in; # substitute your domain name to match
    charset     utf-8;

    # Django media
    location /media  {
        alias /path/to/cloned/repo/AirportProject/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /path/to/cloned/repo/AirportProject/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /path/to/cloned/repo/AirportProject/uwsgi_params; # the uwsgi_params file you installed
    }
}
```
Symlink should be created to this file from /etc/nginx/sites-enabled so nginx can see it.
  
```bash
  sudo ln -s /etc/nginx/sites-available/AirportProject_nginx.conf /etc/nginx/sites-enabled/
```
 <li> Now collect all the static files in the static root directory, through which NGINX will serve all the static files. Execute the command in the project directory.</li><br>
  
  ```bash
  python manage.py collectstatic
  ```
  <li> Then. we use Unix sockets than ports because they carry less overhead. Run this command in the project directory.</li><br>
  
  ```bash
  uwsgi --socket AirportProject.sock --module AirportProject.wsgi --chmod-socket=664
  ```
  
  Note: If you want more flexibility, you can use a separate configuration file with uWSGI. The documentation for that can be found <a href="https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html">here</a>.
  
  <li> Restart the NGINX server, to apply the changes. </li><br>
  
```bash
  sudo /etc/init.d/nginx restart
```

</ol>
<br>
  <h3>DNS management</h3><br>
  Note that in the NGINX configuration file, a placeholder domain is kept which has to be replaced by the domain purchased by the host. Then, a DNS record should be set, with an A record pointing towards the IP of the host computer.
<br><hr>
