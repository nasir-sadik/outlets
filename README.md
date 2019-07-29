
# Oulets Project
[![N|Solid](http://mirosan.com/static/outlet.png)](http://mirosan.com)

Outlets is Python Flask web application that will alow users to create oulets and their items in order to display it to all vistors of this web page.


## The IP address and SSH port

1. IP Address: 35.173.132.98
1. SSH Port  : 2200
1. User      : grader

## Project Demonistration

1. Url : http://mirosan.com/


## Tools To Install

1. **postgresql**: `sudo apt-get install postgresql`
1. **apache2**: `sudo apt install apache2`
1. **python-pip**: `sudo apt-get install`
1. **virtualenv**: `sudo apt-get install virtualenv`
1. **Flask**: `sudo apt-get install Flask`
1. **httplib2**: `sudo apt-get install httplib2`
1. **python3-oauth2client**: `sudo apt-get install python3-oauth2client`
1. **python3-requests**: `sudo apt-get install python3-requests`
1. **python-requests**: `sudo apt-get install python-requests`
1. **python3-sqlalchemy**: `sudo apt-get install python3-sqlalchemy`
1. **python3-psycopg2**: `sudo apt-get install python3-psycopg2`

## Cofigurations
### 1. Getting started
 
- Create  [lightsail virtual server instance](https://www.systemfixes.com/2018/12/31/how-to-create-an-aws-lightsail-linux-instance/)
- Download the AWS provided default private key [LightsailDefaultKey-eu-central-1.pem](https://lightsail.aws.amazon.com/ls/webapp/account/keys) 

### 2. Accessing the remote server via SSH
- Log in to ssh ` ssh ubuntu@35.173.132.98 -p 22 -i .ssh/LightsailDefaultKey-eu-central-1.pem`


### 3. Create user grader

- Create new user grader

	```
	# adduser grader
	```

- Add `grader` to the Group `sudo`

	```
	# usermod -aG sudo grader
    # su - grader
    ```
### 4. Changing the SSH Port from 22 to 2200

- Open the `/etc/ssh/sshd_config`:
	
   ```
   # sudo nano /etc/ssh/sshd_config
   # Port 22 change it to Port 2200
   # service ssh restart
   ```
### 5. Set Timezone to UTC

```
# sudo dpkg-reconfigure tzdata
```

### 6. Create SSH key pair

- On your local machine 
```Open Git Bash then type
   $ ssh-keygen
  ```
### 7. Installing a Public Key

- On the remote server

	```
    mkdir .ssh
    sudo touch .ssh/authorized_keys
    sudo nano .ssh/authorized_keys
    ```
    
    ```
    Copy the public key content from the local machine file and save, change the access level
    chmod 700 .ssh
    chmod 644 .ssh/authorized_keys
    ```
### 8. Firewall Configuration

```
sudo ufw allow 2200/tcp
sudo ufw allow www
sudo ufw allow 123/udp
sudo ufw deny 22
sudo ufw default deny incoming
sudo ufw default allow outgoing
```
- Enable firewall and check status
```
sudo ufw enable
sudo ufw status
```


### 10. Cloning the project application

- Navigate to www directory

   ```
   cd /var/www/
   ```
- Create a directory called `online_store`

   ```
   sudo mkdir online_store
   cd online_store
   ```
- Clone your GitHub repository

	```
	sudo git clone https://github.com/nasir-sadik/outlets.git outlet
	```
### 11. Configuring VirtualHost

- Open `outlets.conf`

   ```
   $ sudo nano /etc/apache2/sites-available/outlets.conf
   ```

- Add the following lines

   ```
        <<VirtualHost *:80>
                ServerName 35.173.132.98
                ServerAlias www.mirosan.com
                ServerAdmin info.gobsan@gmail.com
                WSGIScriptAlias / /var/www/online_store/outlets/outlets.wsgi
                <Directory /var/www/online_store/outlets/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/online_store/outlets/static
                <Directory /var/www/online_store/outlets/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
     </VirtualHost>

   ```
   
- Enable the virtual host:

   ```
   $ sudo a2ensite outlets
   ```

- Restart Apache server:

   ```
   $ sudo service apache2 restart
   ```

### 13. Create the .wsgi File

- Create file `outlets.wsgi` and opent

   ```
   $ cd /var/www/online_store/
   $ sudo nano outlets.wsgi
   ```
- Put the following lines to the content of `outlets.wsgi`
    ```
    #!/usr/bin/python3
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/online_store/outlets")

    from outlet import app as application
    application.secret_key = '0vn6i8gjh81agc8bc528hpbdmn95movh'

    ```
        
- Restart Apache

	```
	sudo service apache2 restart
    ```

## Running The Application

- Navigate to the project path
   ```
   $ cd /var/www/online_store/outlets
   ```
- Run the project
   ```
   $ sudo python outlet.py
   ```

## Third-party resources
https://www.systemfixes.com/2018/12/31/how-to-create-an-aws-lightsail-linux-instance/
https://dillinger.io/