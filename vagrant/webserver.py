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
            message += '''<form method='POST' enctype='multipart/form-data' action='/goal'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
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
            message += '''<form method='POST' enctype='multipart/form-data' action='/goal'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message)
            print(message)
            return
        elif self.path.endswith("/restaurant"):
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
                for restaurant in restaurants:
                    name = unicodedata.normalize('NFKD', restaurant.name).encode('ascii','ignore')
                    message += "<li>"
                    message += name
                    message += "</li>"
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
                messagecontent = fields.get('message')
            message = ""
            message += "<html><body>"
            message += " <h2> Okay, how about this: </h2>"
            message += "<h1> %s </h1>" % messagecontent[0]
            message += '''<form method='POST' enctype='multipart/form-data' action='/goal'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
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
