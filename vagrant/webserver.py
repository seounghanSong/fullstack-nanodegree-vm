#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import unicodedata

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/goal"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>Hello!</h1>"
            message += '''<form method='POST' enctype='text/plain' action='/goal'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print(message)
            return
        elif self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>&#161 Hola !</h1>"
            message += '''<form method='POST' enctype='text/plain' action='/goal'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print(message)
            return
        elif self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>Restaurant Registration Page!!</h1>"
            message += "<li>"
            message += "<a href='/restaurants'> Go back </a>"
            message += "</li>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><p>Name</p><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print(message)
            return
        elif self.path.endswith("/restaurants"):
            try:
                restaurants = session.query(Restaurant.name).all()
            except:
                print("Could not getting the names of restaurant from DB")
                self.send_error(404, 'File Not Found: %s' % self.path)

            if restaurants != None:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body>"
                message += "<h2>"
                message += "<a href='/restaurants/new'>Want to Add New One?</a>"
                message += "</h2>"
                for restaurant in restaurants:
                    name = unicodedata.normalize('NFKD', restaurant.name).encode('ascii','ignore')
                    message += "<li>"
                    message += name
                    message += "<ul><a href='/restaurants'>Edit</a></ul>"
                    message += "<ul><a href='/restaurants'>Delete</a></ul>"
                    message += "</li>"
                    message += "</br>"
                message += "</bodt></html>"
                self.wfile.write(message)
                print(message)
                return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messageContent = fields.get('name')
                # Add Restaurant instance into DB
                new_restaurant = Restaurant(name=messageContent[0])
                session.add(new_restaurant)
                session.commit()
                message = ""
                message += "<html><body>"
                message += "<h2> Fill out the Name section </h2>"
                message += "<li>"
                message += "<a href='/restaurants'> Go back </a>"
                message += "</li>"
                message += "<h1> %s </h1>" % messageContent[0]
                message += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><p>Name</p><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
                message += "</body></html>"
            else:
                fields = cgi.parse_multipart(self.rfile, pdict)
                messageContent = fields.get('message')
                message = ""
                message += "<html><body>"
                message += " <h2> Okay, how about this: </h2>"
                message += "<h1> %s </h1>" % messageContent[0]
                message += '''<form method='POST' enctype='text/plain' action='/goal'><h2>What would you like me to say?</h2><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
                message += "</body></html>"
            self.wfile.write(message)
            print(message)
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
