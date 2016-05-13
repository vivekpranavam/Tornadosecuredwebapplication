import tornado.ioloop
import tornado.web
import cgi
import sqlite3
import tornado.template
import os
import sqlite3 as lite
import time

def CreateDB():
    con = lite.connect('db.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'user'")
        x=cur.fetchone()[0]
        print x

        if x==0:
            cur.execute("CREATE TABLE user(userid varchar(10),username varchar(20), password varchar(20),age integer)")
            con.commit()        
        return x       
class MainHandler(tornado.web.RequestHandler):
        def get(self):
                return self.redirect('/login')
class LoginHandler(tornado.web.RequestHandler):
        def get(self):
                return self.render('index.html')
class HomeHandler(tornado.web.RequestHandler):

        def post(self):
                username=self.get_argument("name")
                password=self.get_argument("password")                
                namestr=cgi.escape(username).encode('ascii', 'xmlcharrefreplace')
                con = lite.connect('db.db')
                with con:
                    cur = con.cursor()
                    cmd="SELECT count(*) FROM user WHERE username= ? and password= ?"
                    cur.execute(cmd, (namestr,password))
                    x=cur.fetchone()[0]
                    if x!=0:
                        self.write('<html><body bgcolor="#E6E6FA"><p>Welcome ' + namestr + '</p>'
                                    '<a href="/list">List All The Users</a><br><br>'                                    
                                    '<a href="/prevent">Preventing DOMXSS</a><br><br>'
                                    '<a href="/SQLiload">SQLi Preventing</a><br><br>'
                                    '<a href="/login">Logout</a></body></html>')
                    else:
                        self.write('<html><body><script>alert("Invalid Useraname or Password..!")</script>'
                                   '<a href="/login">BackToLogin</a></body></html>')               
                

class SignupHandler(tornado.web.RequestHandler):
        def get(self):
                return self.render("signup.html")  
        
        def post(self):                              
                username=self.get_argument("fname")
                userid=self.get_argument("userid")
                password=self.get_argument("password")
                age=self.get_argument("age")
                uname=cgi.escape(username).encode('ascii', 'xmlcharrefreplace')                
                con = lite.connect('db.db')
                with con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO user VALUES(?,?,?,?)",(userid,uname,password,age))
                    self.write('<html><body><script>alert("UserRegistration sucess..!")</script>'
                           '<a href="/login">BackToLogin</a></body></html>')    
                               
class ListuserHandler(tornado.web.RequestHandler):
        def get(self):
            con = lite.connect('db.db')
            with con:
                cur = con.cursor()
                x=cur.execute("select username from user")        
                
                for l1 in x:
                        ul=cgi.escape(l1[0]).encode('ascii', 'xmlcharrefreplace')
                        self.write(ul)
class DOMprevent(tornado.web.RequestHandler):
        def get(self):
                return self.render("domprevent.html")
                        
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
settings = {
            "debug": False,
            "template_path": os.path.join(BASE_DIR, "templates"),
            "static_path": os.path.join(BASE_DIR, "static")
        }  
class SQLiLoadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("usercd.html")

class Sqlihandler(tornado.web.RequestHandler):   
    def get(self):        
        userid=self.get_argument("uid")
        #self.write(userid)        
        con=lite.connect('db.db')
        with con:
            con.create_function("sleep", 1, time.sleep)
            cur=con.cursor()            
            cmd="select userid,username from user where userid= ?"           
            x=cur.execute(cmd,(userid,))
            self.write('<html><body><table style="width:25%"><tr><td>USERID</td><td>USERNAME</td></tr>'
                        '</table></body></html>')
            for l1 in x:
                print l1[0]
                print l1[1]
                self.write('<html><body><table style="width:25%"><tr> <td>' + l1[0] + '</td><td>' + l1[1] + '</td></tr>'
                            '</table>'
                            '</body></html>')
                        
                        
def make_app():
        return tornado.web.Application([(r"/login", LoginHandler),(r"/", MainHandler),(r"/home", HomeHandler),(r"/signup",SignupHandler),(r"/prevent",DOMprevent),
            (r"/list",ListuserHandler),(r"/sqli",Sqlihandler),(r"/SQLiload",SQLiLoadHandler)],**settings)
        
if __name__ == "__main__":
    CreateDB()
    app = make_app()
    app.listen(8888)               
    tornado.ioloop.IOLoop.current().start()