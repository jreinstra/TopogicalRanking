import json

GAMES_FILENAME = "games.json"
K = 32


class Game(object):
    def __init__(self, winner, loser):
        """Initializes a new Game object.
            winner: string of team name that won the game
            loser:  string of team name that lost the game
        """
        self.winner = winner
        self.loser = loser
        
    def __repr__(self):
        return "[%s over %s]" % (self.winner, self.loser)
        
class Player(object):
    def __init__(self, name, rating=1500):
        """Initializes a new Player object.
            name:   string of team/player name
            rating: integer elo rating of team/player
        """
        self.name = name
        self.rating = rating
        
        # list of player names that this player is better/worse than
        self.better_than = []
        self.worse_than = []
        
    def process_game(self, game):
        """Updates better_than and worse_than lists to be up-to-date with the
        given game.
        """
        if game.winner == self.name:
            # if player won, make sure loser is only in better_than list
            if game.loser in self.worse_than:
                self.worse_than.remove(game.loser)
            self.better_than.append(game.loser)
        else:
            # if player lost, make sure winner is only in worse_than list
            if game.winner in self.better_than:
                self.better_than.remove(game.winner)
            self.worse_than.append(game.winner)
            
    def __repr__(self):
        return "[%s, bt %s, wt %s]" % (
            self.name,
            len(self.better_than),
            len(self.worse_than)
        )
            
            
def load_games():
    result = load_json(GAMES_FILENAME)
    games = []
    for game in result:
        games.append(Game(
            clean_game_name(game["Winner"]),
            clean_game_name(game["Loser"])
        ))
    return games
    
def load_json(filename):
    f = open(filename, "r")
    result = ""
    for line in f:
        result += line
    return json.loads(result)
        
def clean_game_name(name):
    if ")" in name:
        name = name[name.index(")") + 2:]
    return name

def load_players(games):
    # format: {"Name":Player()}
    players = {}
    
    for game in games:
        if game.winner != '':
            if game.winner not in players:
                players[game.winner] = Player(game.winner)
            players[game.winner].process_game(game)
            
        if game.loser != '':
            if game.loser not in players:
                players[game.loser] = Player(game.loser)
            players[game.loser].process_game(game)
            
        # change elo ranking of both teams from game result
        elo_rank(players, game.winner, game.loser)
    return players

def elo_rank(players, winner, loser):
    # elo ranking calculation taken from:
    # https://goo.gl/4hjgAA
    try:
        r1 = players[winner].rating
        r2 = players[loser].rating
    except KeyError:
        return
    
    r1_t = 10.0 ** (r1 / 400.0)
    r2_t = 10.0 ** (r2 / 400.0)
    
    e1 = 1.0 * r1_t / (r1_t + r2_t)
    e2 = 1.0 * r2_t / (r1_t + r2_t)
    
    s1 = 1
    s2 = 0
    
    r1 = r1 + (1.0 * K * (s1 - e1))
    r2 = r2 + (1.0 * K * (s2 - e2))
    
    players[winner].rating = r1
    players[loser].rating = r2

def find_next_best(current, players, before=[]):
    if current in before:
        return sorted(
            before[before.index(current):],
            key=lambda x: x.rating,
            reverse=True
        )
    else:
        before.append(current)
        
    w_len = 0
    w_exist = []
    for team in current.worse_than:
        if team in players:
            w_len += 1
            w_exist.append(team)
            
    if w_len == 0:
        return current
    else:
        return find_next_best(players[w_exist[0]], players, before=before)
    


def main():
    games = load_games()
    players = load_players(games)
    
    ranked = []
    while len(players) > 0:
        current = players.items()[0][1]
        best = find_next_best(current, players)
        if isinstance(best, Player):
            ranked.append(best)
            players.pop(best.name, None)
        else:
            for player in best:
                if player not in ranked:
                    ranked.append(player)
                players.pop(player.name, None)
    print ranked
    
main()