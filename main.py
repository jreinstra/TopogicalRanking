import json
import math

K = 32

def clean_name(name):
    if ")" in name:
        name = name[name.index(")") + 2:]
    return name


f = open("games.json", "r")
result = ""
for line in f:
    result += line
    
games = json.loads(result)
players = {} # {"CollegeName":1100}

for game in games:
    names = []
    for key in ["Winner", "Loser"]:
        name = clean_name(game[key])
        names.append(name)
        if players.get(name) == None:
            players[name] = 1500
        
    # elo ranking calculation taken from:
    # https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/
    r1 = players[names[0]]
    r2 = players[names[1]]
    
    r1_t = 10.0 ** (r1 / 400.0)
    r2_t = 10.0 ** (r2 / 400.0)
    #print r1, r2
    
    e1 = 1.0 * r1_t / (r1_t + r2_t)
    e2 = 1.0 * r2_t / (r1_t + r2_t)
    #print e1, e2
    
    s1 = 1
    s2 = 0
    
    r1 = r1 + (1.0 * K * (s1 - e1))
    r2 = r2 + (1.0 * K * (s2 - e2))
    #print r1_new, r2_new
    
    #r1 = math.log(r1_new, 10) * 400.0
    #r2 = math.log(r2_new, 10) * 400.0
    #print r1, r2
    
    players[names[0]] = r1
    players[names[1]] = r2
    #break
    
    
sorted_results =  sorted(players, key=players.get)
N = len(players)
for i in range(0, N):
    player = sorted_results[i]
    buffer_str = " " * (30 - len(player) - len(str(N - i)))
    print str(N - i) + ".", player, buffer_str + str(players[player])