import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask.globals import current_app
from pymongo import MongoClient
from random import choice

app = Flask("GDPScoreboard")

# To change accordingly 
# print(os.environ)
client = MongoClient(os.environ["MONGO_PORT_27017_TCP_ADDR"], 27017)
mongo = client.gdp
password = os.environ["PASSWORD"]

@app.route("/")
def index():
    current_challenge = get_current_challenge()

    last_team = get_last_team()

    first_bloods = mongo.firstbloods.find()

    return render_template("index.html",teams_number=mongo.teams.count(), current_challenge=current_challenge, last_team=last_team, first_bloods=first_bloods)




@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    path=path.split("/")
    if len(path)==2:
        challenge=path[0]
        group=path[1]
        if challenge in ["1","2","3","4","5","6"] and group in ["1","2"]:
            return scoreboard(challenge,group)

    
    return 'Uuuh, well that\'s awkward, you just 404\'d'

def scoreboard(challenge,group):
    teams=mongo.teams.find()

    current_challenge = get_current_challenge()

    last_team = get_last_team()


    first_blood=mongo.firstbloods.find_one({"challenge":str(challenge),"group":group})
    if first_blood:
        first_blood=first_blood["team"]
    else:
        first_blood=-1

    
    if group=='1':
        teams = teams[:last_team]
    else:
        teams = teams[last_team:]

    split_teams=[]
    for team in teams:
        t={"team":team["team"] , "solved":team[str(challenge)] if str(challenge) in team else False }
        if team["team"]==first_blood:
            t["first_blood"]=True
        split_teams.append(t)

    return render_template("scoreboard.html",teams=split_teams, current_challenge=current_challenge)



@app.route("/settings")
def settings():
    current_challenge = get_current_challenge()

    last_team = get_last_team()

    return render_template("settings.html", teams_number=mongo.teams.count(), current_challenge=current_challenge,last_team=last_team)


@app.route("/new_team", methods=["POST"])
def new_team():
    if request.form["password"] and request.form["number"]:
        if (request.form["password"]==password and request.form["number"]!=""):
            teams=[]
            tokens_datasheet=[]
            tokens_wifi=[]
            tokens_mqtt=[]
            for i in range(int(request.form["number"])):

                data = {
                    "team": mongo.teams.count()+i+1,
                    "1": False,
                    "2": False,
                    "3": False,
                    "4": False,
                    "5": False,
                    "6": False
                }
                teams.append(data)
                token = {
                    "used_by_team":0,
                    "value":''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(6)])
                }
                tokens_datasheet.append(token)

                token = {
                    "team":i+1,
                    "value":''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(6)])
                }
                tokens_wifi.append(token)

                token = {
                    "team":i+1,
                    "value":''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(6)])
                }
                tokens_mqtt.append(token)

            mongo.teams.insert_many(teams)
            mongo.tokens_datasheet.insert_many(tokens_datasheet)
            mongo.tokens_wifi.insert_many(tokens_wifi)
            mongo.tokens_mqtt.insert_many(tokens_mqtt)

    return redirect("/settings")

@app.route("/challenge", methods=["POST"])
def change_challenge():
    if request.form["password"] and request.form['challenge']:
        if (request.form["password"]==password and request.form['challenge']!=""):
            mongo.settings.update_one({"tag":"current_challenge"},{"$set":{"value":int(request.form['challenge'])}})

    return redirect(url_for("settings"))

@app.route("/last_team", methods=["POST"])
def last_team():
    if request.form["password"] and request.form['last_team']:
        if (request.form["password"]==password and request.form['last_team']!=""):
            mongo.settings.update_one({"tag":"last_team"},{"$set":{"value":int(request.form['last_team'])}})
    return redirect(url_for("settings"))

@app.route("/success", methods=["POST"])
def success():
    if request.form["password"] and request.form['team'] and request.form["challenge"]:
        if (request.form["password"]==password and request.form['team']!="" and request.form["challenge"]!="" and request.form["challenge"] in ["1", "2", "3", "4"]):
            mongo.teams.update_one({"team":int(request.form['team'])},{"$set":{request.form["challenge"]:True}})

            if mongo.firstbloods.find_one({"challenge":request.form["challenge"],"group":get_group(request.form["team"])})==None:
                mongo.firstbloods.insert_one({"challenge":request.form["challenge"],"group":get_group(request.form["team"]),"team":int(request.form["team"])})

    return redirect(url_for("settings"))






def get_last_team():
    last_team = mongo.settings.find_one({"tag":"last_team"})
    if last_team==None:
        mongo.settings.insert_one({"tag":"last_team","value":0})
        last_team=0
    else:
        last_team=last_team["value"]
    return last_team


def get_current_challenge():
    current_challenge = mongo.settings.find_one({"tag":"current_challenge"})
    if current_challenge==None:
        mongo.settings.insert_one({"tag":"current_challenge","value":1})
        current_challenge=1
    else:
        current_challenge=current_challenge["value"]
    return current_challenge
    

def get_group(team):
    last_team = get_last_team()
    return "1" if int(team)<=last_team else "2"








# Token RX/Datasheet challenge
@app.route("/tokens-datasheet", methods=["GET"])
def add_token():
    tokens = [token["value"] for token in mongo.tokens_datasheet.find({'used_by_team':0})]
    return jsonify(tokens)


@app.route("/deposit", methods=["GET"])
def deposit():
    current_challenge = get_current_challenge()
    return render_template("deposit.html",current_challenge=current_challenge)


@app.route("/submit_datasheet", methods=["POST"])
def submit_datasheet():
    if request.form['token'] and request.form['team']:
        if request.form['token']!="" and request.form['team']!="":
            available_tokens = [token["value"] for token in mongo.tokens_datasheet.find({'used_by_team':0})]
            success_teams = [token["used_by_team"] for token in mongo.tokens_datasheet.find({'used_by_team':{"$ne":0}})]
            print("###",success_teams)
            tokens = [token["value"] for token in mongo.tokens_datasheet.find()]
            token = request.form['token']
            team= int(request.form['team'])
            challenge="1"
            if (token!="" and team!=""):

                if token in available_tokens:
                    if team in success_teams:
                        return "Your team already validated this challenge!"
                else:
                    if token in tokens:
                        return "This token has already been used!"
                    else:
                        return "Bad token! Go to a station to retrieve a valid token!"
            mongo.teams.update_one({"team":team},{"$set":{challenge:True}})
            mongo.tokens_datasheet.update_one({"value":token},{"$set":{"used_by_team":team}})

            if mongo.firstbloods.find_one({"challenge":challenge,"group":get_group(team)})==None:
                mongo.firstbloods.insert_one({"challenge":challenge,"group":get_group(team),"team":int(team)})
            return "Valid token"
    return 'Bad request'
    


# PWM value challenge
@app.route("/pwm",methods=["POST"])
def pwm_challenge():
    challenge="2"
    print("Your data was "+repr(request.data.decode()),flush=True)
    try:
        if len(request.data.decode().split("#"))==3:
            team=int(request.data.decode().split("#")[0])
            guess=int(request.data.decode().split("#")[1])
            true=int(request.data.decode().split("#")[2])
            print("Your parameters were: "+str(team)+" "+str(guess)+" "+str(true),flush=True)
            
            if abs(true-guess) <= 30:
                print("WELL DONE",flush=True)
                mongo.teams.update_one({"team":team},{"$set":{challenge:True}})

                if mongo.firstbloods.find_one({"challenge":challenge,"group":get_group(team)})==None:
                    mongo.firstbloods.insert_one({"challenge":challenge,"group":get_group(team),"team":int(team)})
                return "Well done!"
            else:
                print("Too big of a difference! It was "+str(true-guess),flush=True)

        else:
            print("There is a problem in parameters:",request.data,flush=True)
            return "You are missing either your team or your token in parameters"
        return 'Bad request'
    except Exception as e:
        print(e,flush=True)
        print("Your data was ",request.data,flush=True)
        return "There was en error, here is is your request form: "+str(request.form)+" and data: "+request.data.decode()





# Wifi/http challenge
@app.route("/wifi-challenge",methods=["POST"])
def wifi_challenge():
    challenge="3"
    try:
        if len(request.data.decode().split("#"))==2:
            team=int(request.data.decode().split("#")[0])
            token=request.data.decode().split("#")[1]
            if team!="" and token!="":
                possible_tokens = list(mongo.tokens_wifi.find({'value':token}))
                print(possible_tokens,flush=True)
                if possible_tokens and len(list(possible_tokens))>0:
                    document=possible_tokens[0]
                    if document["team"]==team:
                        mongo.teams.update_one({"team":team},{"$set":{challenge:True}})

                        if mongo.firstbloods.find_one({"challenge":challenge,"group":get_group(team)})==None:
                            mongo.firstbloods.insert_one({"challenge":challenge,"group":get_group(team),"team":int(team)})
                        return "Well done!"
                    else:
                        return "Your token is only for your team!"
                else:
                    return "Bad token!"
        else:
            return "You are missing either your team or your token in parameters"
        return 'Bad request'
    except Exception as e:
        print(e,request.data,flush=True)
        return "There was en error, here is is your request form: "+str(request.form)+" and data: "+request.data.decode()


# MQTT sub challenge
@app.route("/submit_mqqt_sub", methods=["POST"])
def submit_mqqt_sub():
    if request.form['token'] and request.form['team']:
        if request.form['token']!="" and request.form['team']!="":
            team=int(request.form['team'])
            token=request.form['token']
            challenge= "4"
            possible_tokens = list(mongo.tokens_mqtt.find({'value':token}))
            print(possible_tokens,flush=True)
            if possible_tokens and len(list(possible_tokens))>0:
                document=possible_tokens[0]
                if document["team"]==team:
                    mongo.teams.update_one({"team":team},{"$set":{challenge:True}})

                    if mongo.firstbloods.find_one({"challenge":challenge,"group":get_group(team)})==None:
                        mongo.firstbloods.insert_one({"challenge":challenge,"group":get_group(team),"team":int(team)})

                    return "Well done!"
                else:
                    return "Your token is only for your team!"
            else:
                return "Bad token!"
    return 'Bad request'


@app.route("/mqtttokengen", methods=["GET"])
def mqtttokengen():
    if mongo.tokens_mqtt.count()==0:
        tokens_mqtt=[]
        for i in range(mongo.teams.count()):
            token = {
                "team":i+1,
                "value":''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(6)])
            }
            tokens_mqtt.append(token)

        mongo.tokens_mqtt.insert_many(tokens_mqtt)

    return redirect("/settings")




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
