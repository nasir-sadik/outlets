
# Oulets Project
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

Outlets is Python Flask web application that will alow users to create oulets and their items in order to display it to all vistors of this web page.


## The IP address and SSH port

1. IP Address: 35.173.132.98
1. SSH Port  : 2200
1. User      : grader

## Project Demonistration

1. Url : http://mirosan.com/


## Tools To Install

1. postgresql
1. apache2
1. python-pip
1. virtualenv
1. Flask
1. httplib2
1. python3-oauth2client
1. python3-requests
1. python-requests
1. python3-sqlalchemy
1. python3-psycopg2

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

## Third-party resources
https://www.systemfixes.com/2018/12/31/how-to-create-an-aws-lightsail-linux-instance/