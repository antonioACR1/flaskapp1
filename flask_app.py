


######



from flask import Flask, render_template,request,json
from flaskext.mysql import MySQL
import MySQLdb
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
import pandas as pd

mysql=MySQL()

app=Flask(__name__)
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='password123'
app.config['MYSQL_DATABASE_DB']='suggestions'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('website.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('nombre_edad.html')

#mysql> create definer=`root`@`localhost` procedure `sp_createUser8`(in p_name vrchar(255),in p_age int(11), in p_country varchar(255),in p_answer1 int(11),in p_answer2 int(11), in p_answer3 int(11),in p_answer4 int(11), in p_answer5 int(11), in p_song1 varchar(1000), in p_song2 varchar(1000), in p_song3 varchar(1000),in p_link1 varchar(1000),in p_link2 varchar(1000), in p_link3 varchar(1000))
#    -> begin insert into answers (age,country,sex,answer1,answer2,answer3,answer4,answer5,song1,song2,song3,link1,link2,link3) values (p_age,p_country,p_sex,p_answer1,p_answer2,p_answer3,p_answer4,p_answer5,p_song1,p_song2,p_song3,p_link1,p_link2,p_link3); end
  

@app.route('/signUp',methods=['POST','GET'])
def signUp():
        _age = request.form['inputAge']
        _country=request.form['inputCountry']
        _sex=request.form['inputSex']
        _answer1=request.form['inputAnswer1']
        _answer2=request.form['inputAnswer2']
        _answer3=request.form['inputAnswer3']
        _answer4=request.form['inputAnswer4']
        _answer5=request.form['inputAnswer5']
        _song1=request.form['inputSong1']
        _song2=request.form['inputSong2']
        _song3=request.form['inputSong3']
        _link1=request.form['inputLink1']
        _link2=request.form['inputLink2']
        _link3=request.form['inputLink3']
        if _age and _country and _sex and _answer1 and _answer2 and _answer3 and _answer4 and _answer5 and _song1 and _song2 and _song3 and _link1 and _link2 and _link3:
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.callproc('sp_createUser8',(_age,_country,_sex,_answer1,_answer2,_answer3,_answer4,_answer5,_song1,_song2,_song3,_link1,_link2,_link3))
            data=cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'html':'<span>All fields good !!</span>'})
            else:
                return json.dumps({'html':'<span>Enter the required fields</span>'})
   
#construct predictive model

@app.route('/suggestion')    
def suggestion():
	db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="password123", db="suggestions")
	df = pd.read_sql('SELECT age,country,sex,answer1,answer2,answer3,answer4,answer5,song1,link1 FROM answers WHERE ID != (SELECT MAX(ID) FROM answers)',con=db)    
	df['country']=df['country'].astype('str')
	le_country=preprocessing.LabelEncoder()
	df['country_numeric']=le_country.fit_transform(df['country'])
#ASEGURARSE QUE HAY UNA OBSERVACION POR CADA PAIS EN EL TRAINING 
	df_train=df[["age","country_numeric","sex","answer1","answer2","answer3","answer4","answer5"]]
	y_train=pd.read_sql('SELECT suggestion FROM answers WHERE ID != (SELECT MAX(ID) FROM answers WHERE suggestion IS NOT NULL)',con=db)     
	modelo=DecisionTreeClassifier()
	modelo.fit(df_train,y_train)
#Prediction
	new_observation= pd.read_sql('SELECT age,country,sex,answer1,answer2,answer3,answer4,answer5 FROM answers WHERE ID = (SELECT MAX(ID) FROM answers)',con=db) 
	new_observation['country_numeric']=le_country.transform(new_observation['country'])
	df_test=new_observation[['age','country_numeric','sex','answer1','answer2','answer3','answer4','answer5']]
	suggestion_numeric=modelo.predict(df_test)[0]
#getting name and link of the suggestion
	le_song=preprocessing.LabelEncoder()
	song_numeric=le_song.fit_transform(df['song1'])
	le_link=preprocessing.LabelEncoder()
	link_numeric=le_link.fit_transform(df['link1'])
	song=le_song.inverse_transform(suggestion_numeric)
	link=le_link.inverse_transform(suggestion_numeric)
	return render_template('suggested_song.html',song=song,link=link)




if __name__ == "__main__":
    app.run(debug=True)







