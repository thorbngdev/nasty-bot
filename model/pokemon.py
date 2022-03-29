class Pokemon:
    def __init__(self, json):
        self.id = json['id']
        self.name = json['name']
        self.pretty_name = f'**{self.name.capitalize()}**'
        self.front_sprite = json['sprites']['front_default']
        self.back_sprite = json['sprites']['back_default']
        self.shiny_front_sprite = json['sprites']['front_shiny']
        self.shiny_back_sprite = json['sprites']['back_shiny']
        self.type = json['types']
        self.type_str = ''
        for poke_type in self.type:
            self.type_str += poke_type['type']['name']
            if len(self.type) == 2 and self.type_str.count('/') == 0:
                self.type_str += '/'
        self.stats = json['stats']
        self.hp = self.stats[0]['base_stat']
        self.attack = self.stats[1]['base_stat']
        self.defense = self.stats[2]['base_stat']
        self.special_attack = self.stats[3]['base_stat']
        self.special_defense = self.stats[4]['base_stat']
        self.speed = self.stats[5]['base_stat']