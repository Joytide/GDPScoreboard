import time
import os
from pymongo import MongoClient
import paho.mqtt.client as paho
from random import randrange
import math

broker="mosquitto"

mongoclient = MongoClient(os.environ["MONGO_PORT_27017_TCP_ADDR"], 27017)
mongo = mongoclient.gdp

def on_message(client, userdata, message):
    try:
        topic = message.topic
        if len(topic.split("/"))==3:
            if topic.split("/")[0]=="challenge5":
                team = int(topic.split("/")[1])
                mesure = topic.split("/")[2]
                value = round(float(message.payload),1)
                if mesure == "temp" or mesure == "hum":
                    print("Team attempt:",team,mesure,":",value)

                    if mongo.mqtt_pub.find_one({"team":team})==None:
                        mongo.mqtt_pub.insert_one({"team":team,mesure:value})
                    else:
                        mongo.mqtt_pub.update_one({"team":team},{"$set":{mesure:value}})
                    
                    if team != 0:
                        admin_values = mongo.mqtt_pub.find_one({"team":0})
                        if admin_values and "temp" in admin_values and "hum" in admin_values:
                            correct_temp = admin_values["temp"]
                            correct_hum = admin_values["hum"]
                        else:
                            raise Exception("No admin input yet")
                        
                        team_values = mongo.mqtt_pub.find_one({"team":team})
                        if team_values and "temp" in team_values and "hum" in team_values:
                            if abs(team_values["temp"]-correct_temp)<=2 and abs(team_values["hum"]-correct_hum)<=10:
                                challenge="5"
                                mongo.teams.update_one({"team":team},{"$set":{challenge:True}})

                                if mongo.firstbloods.find_one({"challenge":challenge,"group":get_group(team)})==None:
                                    mongo.firstbloods.insert_one({"challenge":challenge,"group":get_group(team),"team":int(team)})
                                print("Correct values!")
                            else:
                                raise Exception("Bad Values for team "+str(team))
                        else:
                            raise Exception("Not all value available for team "+str(team))
                else:
                    raise Exception("Bad topic: "+topic+" for team "+str(team))

            elif topic.split("/")[0]=="challenge6":
                if topic.split("/")[2] == "submit":
                    team = int(topic.split("/")[1])
                    value = int(message.payload)
                    document = mongo.mqtt_calc.find_one({"team":team})
                    if document!=None:
                        
                            print("Team:",team,"Value :",value)
                            
                            if document["result"]==value:
                                print("Correct values!")

                                level = document["level"]+1

                                if level==9:
                                    challenge="6"
                                    mongo.teams.update_one({"team":team},{"$set":{challenge:True}})

                                    if mongo.firstbloods.find_one({"challenge":challenge,"group":get_group(team)})==None:
                                        mongo.firstbloods.insert_one({"challenge":challenge,"group":get_group(team),"team":int(team)})
                                    print("Well done!")
                                
                                else:
                                    a = randrange(10,50)
                                    b = randrange(1,20)
                                    x = randrange(1,5)

                                    max_level = 1
                                    if "max_level" in document:
                                        if level>document["max_level"]:
                                            max_level = level

                                    if x==1:
                                        task = str(a)+" x "+str(b)
                                        result = a*b
                                    elif x==2:
                                        task = str(a)+" XOR "+str(b)
                                        result = a^b
                                    elif x==3:
                                        task = str(b)+"!"
                                        result = math.factorial(str(b))
                                    elif x==4:
                                        task = str(a)+" << "+str(b)
                                        result = a<<b

                                    client.publish("challenge6/"+str(team)+"/task",task)
                                    mongo.mqtt_calc.update_one({"team":team},{"$set":{"task":task,"result":result,"level":level,"max_level":max_level}})
                            else:
                                raise Exception("Wrong answer")
                elif topic.split("/")[2] == "task":
                    pass
                else:
                    raise Exception("Bad topic "+topic)
            elif topic.split("/")[0]=="challenge4":
                pass
            else:
                pass
        else:
            pass

    

    except Exception as e:
        print("ERROR:",e)


def get_group(team):
    last_team = get_last_team()
    return "1" if int(team)<=last_team else "2"

def get_last_team():
    last_team = mongo.settings.find_one({"tag":"last_team"})
    if last_team==None:
        mongo.settings.insert_one({"tag":"last_team","value":0})
        last_team=0
    else:
        last_team=last_team["value"]
    return last_team


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")







client= paho.Client("admin")
client.on_message=on_message
client.on_connect= on_connect
print("Subscribing for temp and hum in challenge5/<team>/# for all teams ("+str(mongo.teams.count())+")")
client.username_pw_set(username="admin",password="eKKUVjwFkfxtHk8U")
client.connect(broker)
client.loop_start()
count=60
while True:
    if count%10==0:
        for team in range(1,mongo.teams.count()):
            a = randrange(1,100)
            b = randrange(1,100)
            task = str(a)+" + "+str(b)
            client.publish("challenge6/"+str(team)+"/task",task)

            # Reset mongo task and level
            if mongo.mqtt_calc.find_one({"team":team})==None:
                mongo.mqtt_calc.insert_one({"team":team,"task":task,"result":a+b,"level":1})
            else:
                mongo.mqtt_calc.update_one({"team":team},{"$set":{"task":task,"result":a+b,"level":1}})
        print("Reseting tasks on challenge6/<team>/task")
    
    if count==60:
        print("Publishing tokens on challenge4/<team>/token")
        tokens = mongo.tokens_mqtt.find()
        for token in tokens:
            client.publish("challenge4/"+str(token["team"])+"/token",token["value"]) #publish
        count=0

    count+=1
    client.subscribe("#")
    
    
    time.sleep(1) # on_message will proc even in on sleep
    


