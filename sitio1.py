
from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def edad():
    edad=request.args.get("country")
    return edad


if __name__ == "__main__":
    app.run()


from flask import render_template,Flask
from string import Template

sitio1=Flask(__name__)

html='''<html> <head>
<p> Roxana is:</p>
<h1> $code</h1>
<p>years old</p>
</head>
</html>'''

s=Template(html).safe_substitute(code=27)

@sitio1.route("/")
def main():
    return render_template(s)

if __name__=="__main__":
    sitio1.run()

@sitio1.route("/")
def main():
    return render_template()
    
if __name__=="__main__":
    sitio1.run()
    
from string import Template    


s=Template(html).safe_substitute(code=27)
print(s)


app=Flask(__name__)
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='password123'
app.config['MYSQL_DATABASE_DB']='suggestions'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('website.html')
    
if __name__=="__main__":
    app2.run()


