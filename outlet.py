from flask import Flask, render_template, url_for, flash
from flask import redirect, request, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from database_setup import Base, Outlet, Item, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import httplib2
import requests
import json
import random
import string


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

app.config['SECRET_KEY'] = '0vn6i8gjh81agc8bc528hpbdmn95movh'

engine = create_engine('sqlite:///outletDB.db?check_same_thread=False')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token


@app.route('/login')
def Login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    print data['email']
    if session.query(User).filter_by(email=data['email']).count() != 0:
        current_user = session.query(User).filter_by(email=data['email']).one()
    else:
        newUser = User(name=data['name'],
                       email=data['email'])
        session.add(newUser)
        session.commit()
        current_user = newUser

    login_session['user_id'] = current_user.id
    print current_user.id

    output = ''
    output += login_session['username']
    output += login_session['picture']
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % access_token)
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None, headers={
                  'content-type': 'application/x-www-form-urlencoded'})[0]

    print url
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successfully logged out", "success")
        return redirect('/index')
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show all outlets
@app.route("/")
@app.route("/index")
def showOutlet():
    # Show all outlet
    outlet = session.query(Outlet).all()
    items = session.query(Item).all()
    return render_template('index.html', outlet=outlet,
                           items=items)


# Show New Items
@app.route("/")
@app.route("/item/new/")
def showNewItem():

    return render_template('new_item.html')

# Display outlet Item


@app.route('/outlet/<int:outlet_id>/<string:outlet_name>/')
@app.route('/outlet/<int:outlet_id>/<string:outlet_name>/item/')
def showItem(outlet_id, outlet_name):
    AllOutlets = session.query(Outlet).all()
    items = session.query(Item).filter_by(
        outlet_id=outlet_id).all()
    countitem = len(items)
    flash('Please click on OUTLETS list panel header to show all items.',
          "info")
    return render_template('index.html', outlet=AllOutlets,
                           items=items, filter=outlet_name,
                           itemCount=countitem)

# Create new outlet
@app.route('/outlet/new/', methods=['GET', 'POST'])
def createNewOutlet():
    if 'username' not in login_session:
        return redirect('/login')
    user_id = login_session['user_id']
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        outletExist = session.query(Outlet).filter_by(
            name=request.form['outlet_name']).all()

        if outletExist:
            flash('Sorry, an Outlet with the name (%s) exists' %
                  request.form['outlet_name'], "error")
            return render_template('new_outlet.html')

        newoutlet = Outlet(name=request.form['outlet_name'],
                           user_id=user_id)
        session.add(newoutlet)
        flash('Successfully created', "success")
        session.commit()
        return redirect(url_for('showOutlet'))
    else:
        return render_template('new_outlet.html')


# Create new item

@app.route('/outlet/item/new', methods=['GET', 'POST'])
def createNewItem():
    # check if username is logged in
    if 'username' not in login_session:
        return redirect('/login')
    user_id = login_session['user_id']
    alloutlet = session.query(Outlet).filter_by(user_id=user_id)

    if request.method == 'POST':
        if request.form['item_outlet_id'] == "":
            flash('Please select an outlet from the oulet list.', "error")
            return render_template('new_item.html',
                                   alloutlet=alloutlet)
        outlet = session.query(Outlet).filter_by(
            id=request.form['item_outlet_id']).one()
        if outlet.user_id != login_session['user_id']:
            flash('Sorry, you are not allowed to Add a itme to outlet id %s' %
                  request.form['item_outlet_id'], "error")
            return render_template('new_item.html',
                                   alloutlet=alloutlet)
        itemExistance = session.query(Item).filter_by(
            name=request.form['item_name'],
            outlet_id=request.form['item_outlet_id']).all()
        if itemExistance:
            flash("""Sorry, an item with the name (%s)
                    exists under the outlet you selected """ %
                  request.form['item_name'], "error")
            return render_template('new_item.html',
                                   alloutlet=alloutlet)

        newItem = Item(name=request.form['item_name'],
                       description=request.form['item_description'],
                       price=request.form['item_price'],
                       outlet_id=request.form['item_outlet_id'],
                       user_id=user_id)
        session.add(newItem)
        flash('Successfully created', 'success')
        session.commit()
        return redirect(url_for('showOutlet'))
    else:
        return render_template('new_item.html', alloutlet=alloutlet)


# Selecting a specific item
@app.route('/outlet/<string:outlet_name>/<string:item_name>/')
def showSpecificItem(outlet_name, item_name):
    outlet = session.query(Outlet).filter_by(
        name=outlet_name).one()
    item = session.query(Item).filter_by(
        name=item_name, outlet_id=outlet.id).one()
    return render_template('specific_item.html',
                           item=item, outlet=outlet)


# Delete outlet
@app.route('/outlet/<int:outlet_id>/outlet/delete',
           methods=['GET', 'POST'])
def deleteOutlet(outlet_id):
    # check if username is logged in
    if 'username' not in login_session:
        return redirect('/login')
    deloutlet = session.query(Outlet).filter_by(
        id=outlet_id).one()
    hasItems = session.query(Item).filter_by(
        outlet_id=outlet_id).all()
    if deloutlet.user_id != login_session['user_id']:
        flash('Sorry, you are not allowed to Delete', "error")
        return redirect(url_for('showOutlet'))
    if hasItems:
        flash('The outlet (%s) has item(s), first delete all its items' %
              deloutlet.name, "error")
        return redirect(url_for('showOutlet'))
    if request.method == 'POST':
        session.delete(deloutlet)
        session.commit()

        flash('Successfully Deleted', 'success')
        return redirect(url_for('showOutlet'))
    else:
        return render_template('delete_outlet.html',
                               deloutlet=deloutlet)

# Edit outlet
@app.route('/outlet/<int:outlet_id>/outlet/edit',
           methods=['GET', 'POST'])
def editOutlet(outlet_id):
    # check if username is logged in
    if 'username' not in login_session:
        return redirect('/login')
    editoutlet = session.query(Outlet).filter_by(
        id=outlet_id).one()
    if editoutlet.user_id != login_session['user_id']:
        flash('Sorry, you are not allowed to edit', "error")
        return redirect(url_for('showOutlet'))
    if request.method == 'POST':
        if request.form['outlet_name']:
            editoutlet.name = request.form['outlet_name']
            session.add(editoutlet)
            session.commit()
            flash('Successfully Edited', 'success')
            return redirect(url_for('showOutlet'))
    else:
        return render_template('edit_outlet.html',
                               outlet_id=outlet_id,
                               editoutlet=editoutlet)


# Edit existing item
@app.route('/outlet/<int:outlet_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(outlet_id, item_id):
    # check if username is logged in
    if 'username' not in login_session:
        return redirect('/login')
    items = session.query(Item).filter_by(id=item_id).one()
    if items.user_id != login_session['user_id']:
        flash('Sorry, you are not allowed to edit', "error")
        return redirect(url_for('showSpecificItem',
                                outlet_name=items.outlet.name,
                                item_name=items.name))
    if request.method == 'POST':
        if request.form['item_name']:
            items.name = request.form['item_name']
        if request.form['item_description']:
            items.description = request.form['item_description']
        if request.form['item_price']:
            items.price = request.form['item_price']
            session.add(items)
            session.commit()
            flash('Successfully Edited', 'success')
            return redirect(url_for('showItem',
                                    outlet_id=outlet_id,
                                    outlet_name=items.outlet.name))
    else:
        return render_template('edit_item.html', outlet_id=outlet_id,
                               item_id=item_id, item=items)

# Delete  item
@app.route('/outlet/<int:outlet_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(outlet_id, item_id):

    # check if username is logged in
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(id=item_id).one()
    if item.user_id != login_session['user_id']:
        flash('Sorry, you are not allowed to delete outlet id %s' %
              outlet_id, "error")
        return redirect(url_for('showSpecificItem',
                                outlet_name=item.outlet.name,
                                item_name=item.name))

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Successfully Deleted', 'success')
        return redirect(url_for('showOutlet'))

    else:
        return render_template('delete_item.html',
                               outlet_id=outlet_id,
                               item_id=item_id,
                               item=item)


# Outlets with their item in json
@app.route('/json')
def jSONView():
    """Returns JSON for all outlets and their items"""
    outlet = session.query(Outlet).options(
        joinedload(Outlet.items)).all()
    return jsonify(Outlet=[dict(o.serialize, items=[i.serialize
                                                    for i in o.items])
                           for o in outlet])

# returns all outlets in json
@app.route('/outlet/json')
def outletJSON():
    outlets = session.query(Outlet).all()
    return jsonify(Outlet=[c.serialize for c in outlets])


# returns all items in json
@app.route('/item/json')
def itemsJSON():

    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
