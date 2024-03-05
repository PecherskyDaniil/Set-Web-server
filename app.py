# import main Flask class and request object
from flask import Flask, request
import json
import random as rand
from hashlib import md5


def createfield():
    field={"cards":[]}
    for id in range(9):
        field["cards"].append({"id":id,"color":int((((rand.random())*10)%3)+1),"shape":int((((rand.random())*10)%3)+1),"fill":int((((rand.random())*10)%3)+1),"count":int((((rand.random())*10)%3)+1)})
    return field

def SetsOnField(data):
    orfield=data["cards"]
    field=[]
    for i in range(len(orfield)):
        field.append(orfield[i].copy())
        field[i]["id"]=0
    sets=[]
    for card1 in range(len(field)-1):
        for card2 in range(card1+1,len(field)):
            cardexample={}
            for parametr in field[0]:
                if (field[card1][parametr]==field[card2][parametr]):
                    cardexample[parametr]=field[card1][parametr]
                else:
                    cardexample[parametr]=6-field[card1][parametr]-field[card2][parametr]
            if (cardexample in field):
                print(cardexample)
                for ind in range(len(field)):
                    if field[ind]==cardexample and ind!=card1 and ind!=card2:
                        sets.append(list(sorted([orfield[card1]["id"],orfield[card2]["id"],orfield[ind]["id"]])))
    return sets

dannue={}
rmlist=[]
whoingame={}
idcounter=0
def fail(message):
    response={"success":"false","exception":{"message":message}}
    response=json.dumps(response)
    return response


def createtoken(nickname,password):
    m=nickname+password
    md5_hash = md5(m.encode("utf8")).hexdigest()
    return md5_hash

# create the Flask app
app = Flask(__name__)

@app.route('/user/login', methods=['POST'])
def logining():
    global dannue
    request_data= request.get_json()
    response={'nickname':dannue[request_data['accessToken']]}
    response=json.dumps(response)
    return response

@app.route('/example', methods=["POST"])
def form_example():
    return str(SetsOnField(rmlist[0]["field"]))

# GET requests will be blocked
@app.route('/user/register', methods=['POST'])
def registration():
    request_data = request.get_json()
    global dannue
    nickname = None
    accesstoken=None
    if request_data:
        if 'nickname' in request_data:
            nickname = request_data['nickname']
        else:
            return fail("No nickname")

        if 'password' in request_data:
            accesstoken =createtoken(nickname,request_data['password'])
        else:
            return fail("No password")
    if nickname in dannue.values():
        return fail("nickname locked")
    dannue[accesstoken]=nickname
    response={"nickname":nickname,"accessToken":accesstoken}
    response=json.dumps(response)
    return response


@app.route('/set/room/create', methods=['POST'])
def roomcreate():
    request_data = request.get_json()
    global dannue
    global rmlist
    global idcounter
    accessToken=None
    if request_data:
        if 'accessToken' in request_data:
            accessToken=request_data['accessToken']
            if accessToken not in dannue:
                return fail("AccessToken not found")
        else:
            return fail("No 'accessToken'")
    rmlist.append({"id":idcounter,"field":createfield(),"users":[]})
    response={"success":"true","exception":"null","gameId":idcounter}
    idcounter+=1
    response=json.dumps(response)
    return response


@app.route('/set/room/list', methods=['POST'])
def roomlist():
    request_data = request.get_json()
    accesstoken=None
    if request_data:
        if 'accessToken' in request_data:
            accesstoken=request_data['accessToken']
            if accesstoken not in dannue:
                return fail("AccessToken not found")
        else:
            return fail("No 'accessToken'")
    response={"games":[]}
    for i in rmlist:
        response["games"].append({"id":i["id"]})
    response=json.dumps(response)
    return response


@app.route('/set/room/enter', methods=['POST'])
def roomenter():
    request_data = request.get_json()
    accesstoken=None
    gameid=None
    if request_data:
        if 'accessToken' in request_data:
            accesstoken=request_data['accessToken']
            if accesstoken not in dannue:
                return fail("AccessToken not found")
        else:
            return fail("No 'accessToken'")
        idinlist=0
        if 'gameId' in request_data:
            gameid=request_data['gameId']
            for i in rmlist:
                if i["id"]==gameid:
                    idinlist=1
            if idinlist==0:
                return fail("Game not found")
        else:
            return fail("No 'gameId'")
    if accesstoken in whoingame:
       for i in rmlist:
           if i["id"]==whoingame[accesstoken]:
               for j in range(len(i["users"])):
                   if dannue[accesstoken] == i["users"][j]["name"]:
                       i["users"].pop(j)
    else:
       for i in rmlist:
           if i["id"]==gameid:
               for j in i["users"]:
                   if dannue[accesstoken] in j["name"]:
                       return fail("user already in room")
               i["users"].append({"name":dannue[accesstoken],"score":0})
    whoingame[accesstoken]=gameid
    response={"success": "true","exception": "null","gameId":gameid }
    response=json.dumps(response)
    return response


@app.route('/set/field', methods=['POST'])
def fieldgeter():
    request_data = request.get_json()
    accesstoken=None
    if request_data:
        if 'accessToken' in request_data:
            accesstoken=request_data['accessToken']
            if accesstoken not in dannue:
                return fail("AccessToken not found")
        else:
            return fail("No 'accessToken'")
    for i in rmlist:
        if i["id"]==whoingame[accesstoken]:
            response=i["field"]
            for user in i["users"]:
                if user["name"]==dannue[accesstoken]:
                    response["score"]=user["score"]
            response["status"]="ongoing"
            reponse=json.dumps(response)
            return response
    return fail("accesstoken not in game")

@app.route('/set/pick', methods=['POST'])
def setpicker():
    request_data = request.get_json()
    accesstoken=None
    cards=[]
    if request_data:
        if 'accessToken' in request_data:
            accesstoken=request_data['accessToken']
            if accesstoken not in dannue:
                return fail("AccessToken not found")
        else:
            return fail("No 'accessToken'")
        if 'cards' in request_data:
            cards=request_data['cards']
            if len(cards)!=3:
                return fail("Wrong Number of cards")
        else:
            return fail("No 'cards'")
    response={}
    udal=[]
    for game in rmlist:
        if game["id"]==whoingame[accesstoken]:
            field=game["field"]
            sets=SetsOnField(field)
            if list(sorted(cards)) in sets:
                for user in game["users"]:
                    if user["name"]==dannue[accesstoken]:
                        user["score"]+=3
                        for card in range(len(game["field"]["cards"])):
                            if game["field"]["cards"][card]["id"] in cards:
                                udal.append(card)
                        for card in range(len(udal)-1,-1,-1):
                            game["field"]["cards"].pop(udal[card])
                        response["isSet"]="True"
                        response["score"]=user["score"]
                        reponse=json.dumps(response)
                        return response
            else:
                response["isSet"]="False"
                response["score"]=0
                response=json.dumps(response)
                return response
    return fail("accesstoken not in game")


@app.route('/set/add', methods=['POST'])
def setadder():
    request_data = request.get_json()
    accesstoken=None
    if request_data:
        if 'accessToken' in request_data:
            accesstoken=request_data['accessToken']
            if accesstoken not in dannue:
                return fail("AccessToken not found")
        else:
            return fail("No 'accessToken'")
    for game in rmlist:
        if game["id"]==whoingame[accesstoken]:
            if len(game["field"]["cards"])<21:
                idcard=game["field"]["cards"][-1]["id"]
                for it in range(3):
                    idcard+=1
                    game["field"]["cards"].append({"id":idcard,"color":int((((rand.random())*10)%3)+1),"shape":int((((rand.random())*10)%3)+1),"fill":int((((rand.random())*10)%3)+1),"count":int((((rand.random())*10)%3)+1)})
                response={"success":"true","exception":"null"}
                response=json.dumps(response)
                return response
            else:
                return fail("too many cards")
    return fail("accesstoken not in game")

@app.route('/set/scores', methods=['POST'])
def setscores():
    request_data = request.get_json()
    accesstoken=None
    if request_data:
        if 'accessToken' in request_data:
            accesstoken=request_data['accessToken']
            if accesstoken not in dannue:
                return fail("AccessToken not found")
        else:
            return fail("No 'accessToken'")
    for game in rmlist:
        if game["id"]==whoingame[accesstoken]:
            response={"success":"true","exception":"null","users":game["users"]}
            response=json.dumps(response)
            return response
    return fail("accesstoken not in game")



