def update_players2(s):
    data = {
            "function": "update_players2",
            "game_name":s.game_name,
            "name" : s.player.name,
            "money": s.player.money,
            "pos": s.player.pos,
            "x": s.player.x,
            "y": s.player.y,
            "interested": s.player.interested,
            "movement": s.player.movement,
            "wait": s.player.wait,
            "juz_sprawdzone":s.player.juz_sprawdzone
        }
        
    act = s.network.send(data)
    s.player = act["player"]
    s.players = act["players"]