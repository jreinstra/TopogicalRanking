# TopogicalRanking
This program uses topological sort to rank college football teams based on a list of Div I NCAA games that occurred in the 2015 season.  The program uses a JSON list of games as input, in the following format:
```
{
  "Rk":1,
  "Winner":"(22) Arizona",
  "WinnerPoints":42,
  "Loser":"Texas-San Antonio",
  "LoserPoints":32
},
```

These games are used to calculate the elo rating of each football team and a list of teams that each team is better than or worse than.  Then, the teams are sorted topologically, with any list of equivalent teams sorted by the elo rating.
