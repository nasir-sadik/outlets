
# Oulets Project

Outlets is web application that will alow users to create oulets and their items in order to display it to all vistors of this web page.


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

## Cofiguration
#### Creating RSA Key Pair
    1. Install Vagrant and VirtualBox
    1. Launch the Vagrant VM (vagrant up)
    1. Write your Flask application locally in the vagrant/catalog directory (which will automatically be synced to /vagrant/catalog within the VM).
    1. Run  `python /vagrant/catalog/online_store/databse_setup.py` , this is for the first time to create database.
    1. Run Run your application within the VM `python /vagrant/catalog/online_store/outlet.py`
    1. Access and test your application by visiting http://localhost:5000 locally
