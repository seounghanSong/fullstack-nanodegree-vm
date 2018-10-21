#!/usr/bin/python3
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine  = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

''' Fake Database Value for testing Route
#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
'''

# TODO: Make separate Restaurnat / MenuItem object extract function for sure
# TODO: Add Flash message when some action is being executed.

# Making an API Endpoint start (Now only GET Request)

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItems = menuItem.serialize)

# Making an API Endpoint end (Now only GET Request)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants = restaurants)
    # return('This page will show all my restaurants')

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created")
        restaurants = session.query(Restaurant).all()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')
    # return('This page will be for making a new restaurant')

@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        editRestaurant.name = request.form['name']
        session.add(editRestaurant)
        session.commit()
        flash("Restaurant Successfully Edited")
        return redirect(url_for('showRestaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('editRestaurant.html', restaurant = restaurant)
    # return("This page will be for editing restaurant %s" % restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deleteRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleteRestaurant)
        session.commit()
        flash("Restaurant Successfully Deleted")
        return redirect(url_for('showRestaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('deleteRestaurant.html', restaurant = restaurant)
    # return('This page will be for deleting restaurant %s' % restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant, menus = items)
    # return('This page is the menu for restaurant %s' % restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id =
            restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New MenuItem Created")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('newMenuItem.html', restaurant = restaurant)
    # return('This page is for making a new menu Item for restaurant %s' % restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        session.add(editItem)
        session.commit()
        flash("Menu Item successfully Edited")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        item = session.query(MenuItem).filter_by(id = menu_id).one()
        return render_template('editMenuItem.html', restaurant = restaurant,
        menu = item)
    # return('This page is for editing menu %s' % menu_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Menu Item successfully Deleted")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        item = session.query(MenuItem).filter_by(id = menu_id).one()
        return render_template('deleteMenuItem.html', restaurant = restaurant,
            menu = item)
    # return('This page is for deleting menu %s' % menu_id)


if __name__ == '__main__':
    app.secret_key = 'restaurant_key' # for developement purpose
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
