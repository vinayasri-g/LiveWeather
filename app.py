from flask import Flask,redirect,render_template,url_for,request,jsonify

import requests,json
from flask_mysqldb import MySQL
from datetime import date
from datetime import datetime
from pywttr import Wttr

app=Flask(__name__)
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']='vinayasri@123'
app.config['MYSQL_DB']='cities'
mysql=MySQL(app)

@app.route('/')
def homereturn():
    return render_template("index.html")
#function for making the place dynamic
def getWeather(city="Vijayawada"):
    try:

        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=6483b1507d395323d6beeebe6421750e"
        
        r = requests.get(url).json() 
        classname=r['weather'][0]['description']
        classname= classname.replace(" ", "-")
        weather={
            'city':city,
            'temperature':round((r['main']['temp'])-273.15,2), 
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
            'time':r['timezone'],
            'humidity':r['main']['humidity'],
            'wind':r['wind']['speed'], 
            'pressure':r['main']['pressure'], 
            'cssClassName':classname
            
        }
        
        return weather
    except:
        weather="city not found"
    return weather


#route for displaying the details such as temp,humid,pressure etc
@app.route('/second',methods=["GET","POST"])
def home():
    if request.method=="POST":
        place=request.form['city']
        weather=getWeather(city=place)
        if weather!='city not found':
            if place.lower() in ['vijayawada','guntur']:
                temperature=weather['temperature']
                humidity=weather['humidity']
                pressure=weather['pressure']
                cursor=mysql.connection.cursor()
                query=f'insert into {place} (temperature,pressure,humidity) values({temperature},{pressure},{humidity})'
                cursor.execute(query)    
                mysql.connection.commit()
                cursor.close()
        return render_template('homepage.html',weather=weather)
    return render_template('homepage.html',weather=getWeather())



# @app.route('/forecast',methods=['GET','POST'])
# def forcast(city):
#     wttr = Wttr(city)
#     forecast = wttr.en()
#     print(forecast.weather[2].avgtemp_c)
# app.run()


#Route for the forecasting the data for the next three days
@app.route('/forecast',methods=["GET","POST"])
def index():
    place='vijayawada'  
    wttr=Wttr(place)
    forecast = wttr.en()
    data=forecast.weather
    day1=data[0]
    day2=data[1]
    day3=data[2]
    
    sunset=print(day1.astronomy[0].sunset)
    print(day1.astronomy[0].sunrise)
    print(day1.avgtemp_c)
    print(day1.hourly[0].humidity)
    print(day1.hourly[0].pressure)
    print(day1.hourly[0].weather_desc[0].value)
    print(day1.date)
    
    
    if request.method=='POST':
        place=request.form['city']    
        wttr=Wttr(place)
        forecast = wttr.en()
        data=forecast.weather
        day1=data[0]
        day2=data[1]
        day3=data[2]
        
       
        return render_template("cards.html",day1=day1,day2=day2,day3=day3)
    return render_template("cards.html",day1=day1,day2=day2,day3=day3)

#Route for the past data diplaying
@app.route('/previous/<place>',methods=["GET","POST"])
def prefore(place):
    cursor=mysql.connection.cursor()
    data=(f"SELECT * from {place}")
    cursor.execute(data)
    option=cursor.fetchall()
    cursor.close()
    if request.method=='POST':
        place=request.form['option']
        cursor=mysql.connection.cursor()
        data=(f"SELECT * from {place}")
        cursor.execute(data)
        option=cursor.fetchall()
        cursor.close()
        return render_template("previousdata.html",place=option)
    return render_template("previousdata.html",place=option)
   
app.run(debug=True)


