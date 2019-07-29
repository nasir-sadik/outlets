
# Oulets Project

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

## Database Structure

The databse contains the following three tables: 
1. **user** - contains all registered users.  
1. **outlet** - contains all outlets information.
1. **item** - contains all items of the outlets.

## Cofigurations
### 1. Creating RSA Key Pair
 
- Create lightsail virtual server instance
- Download the AWS provided default private key `LightsailDefaultKey-eu-central-1.pem`

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
    ```
### 4. Create SSH key pair

- On your local machine 
```Open Git Bash then type
   $ ssh-keygen
  ```