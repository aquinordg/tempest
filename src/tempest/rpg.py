class Character:

    def __init__(self, name, attr):

        self.name = name
        self.attr = attr
        self.hp = attr['health']
        self.readyness = 0

    def __getattr__(self, name):

        return self.attr[name]

    def update(self):

        # Sudden death...
        self.health = self.health - 1
        self.hp = min(self.health, self.hp)

        if self.hp > 0:
            self.readyness = self.readyness + self.speed

    def is_ready(self):

        return self.readyness > 100

    def act(self, allies, enemies, rng):

        assert self.is_ready()
        assert self.hp > 0
        assert self.readyness > 100

        self.readyness = self.readyness - 100

        eactive = [enemy for enemy in enemies if enemy.hp > 0]
        assert len(eactive) > 0
        party = [hero for hero in allies if hero.hp >
                 0 and hero.name != self.name]

        attack_chance = 0.5 * (self.agressiveness + 1)
        cooperation_chance = 0.5 * (self.cooperation + 1)
        leadership_chance = 0.5 * (self.leadership + 1)

        if self.boost == 1 and len(
                party) > 0 and rng.random() < leadership_chance:
            action = 'boost'
        elif self.hit == 1 and (self.hp > 0.9 *
                                self.health or rng.random() < attack_chance):
            if self.combo == 1 and len(
                    party) > 0 and rng.random() < cooperation_chance:
                action = 'combo'
            else:
                action = 'attack'
        elif self.cure == 1 and rng.random() < cooperation_chance:
            action = 'cure'
        else:
            action = 'rest'

        if action == 'attack':
            target = eactive[rng.randint(len(eactive))]
            target.hp = target.hp - \
                (self.attack * self.attack) / (2 * target.defense)
            # print(f'{self.name}(hp={round(self.hp)}/{self.health}) attacked...')
            # if target.hp < 0:
            #     print(f'{target.name} is dead...')
            # else:
            #     print(
            #         f'{target.name}(hp={round(target.hp)}/{target.health}) was hit...')
        elif action == 'combo':
            assert len(party) > 0
            target = eactive[rng.randint(len(eactive))]
            helper = party[rng.randint(len(party))]

            hcooperation_chance = 0.5 * (helper.cooperation + 1)
            if rng.random() < hcooperation_chance:
                dmg = 1.1 * (self.attack + helper.attack)
                helper.readyness = helper.readyness - 100
            else:
                dmg = 0.9 * self.attack

            target.hp = target.hp - (dmg * dmg) / (2 * target.defense)
            # print(f'{self.name}(hp={round(self.hp)}/{self.health}) combo attacked...')
            # if target.hp < 0:
            #     print(f'{target.name} is dead...')
            # else:
            #     print(
            #         f'{target.name}(hp={round(target.hp)}/{target.health}) was hit...')
        elif action == 'cure':
            target = allies[rng.randint(len(allies))]
            target.hp = min(target.health, target.hp + 0.1 * target.health)
            # print(
            #     f'{target.name}(hp={round(target.hp)}/{target.health}) was cured...')
        elif action == 'rest':
            self.hp = min(self.health, self.hp + 0.1 * self.health)
            # print(f'{self.name}(hp={round(self.hp)}/{self.health}) rested...')
        elif action == 'boost':
            helper = party[rng.randint(len(party))]

            dmg = helper.attack * (1 - helper.leadership)

            target = eactive[rng.randint(len(eactive))]
            target.hp = target.hp - (dmg * dmg) / (2 * target.defense)

            # print(f'{self.name}(hp={round(self.hp)}/{self.health}) ordered {helper.name}(hp={round(helper.hp)}/{helper.health}) to attack...')
            # print(f'\tboost: {1 - helper.leadership}x')
            # if target.hp < 0:
            #     print(f'{target.name} is dead...')
            # else:
            #     print(
            #         f'{target.name}(hp={round(target.hp)}/{target.health}) was hit...')
        else:
            raise NotImplemented


class Battle:

    def __init__(self, heroes, enemies, rng):

        self.heroes = heroes
        self.enemies = enemies
        self.iterations = 0.0
        self.rng = rng

    def iterate(self):

        for char in self.heroes + self.enemies:
            char.update()

        ready = [(char, 'hero') for char in self.heroes if char.is_ready()] + \
            [(char, 'enemy') for char in self.enemies if char.is_ready()]

        for char, type in ready:
            if char.hp <= 0 or char.readyness <= 100:
                continue
            self.iterations = self.iterations + 1
            if type == 'hero':
                char.act(self.heroes, self.enemies, self.rng)
            else:
                char.act(self.enemies, self.heroes, self.rng)
            if self.has_ended():
                return

    def has_ended(self):
        if len([enemy for enemy in self.enemies if enemy.hp > 0]) == 0:
            return True

        if len([hero for hero in self.heroes if hero.hp > 0]) == 0:
            return True

        return False

    def score(self):

        assert self.iterations == 0
        while not self.has_ended():
            self.iterate()

        if len([hero for hero in self.heroes if hero.hp > 0]) == 0:
            return 0
        return 1.0 / self.iterations


if __name__ == '__main__':
    import sys
    import pandas as pd
    import numpy as np

    assert len(sys.argv) == 5

    cfilename = sys.argv[1]
    tfilename = sys.argv[2]
    count = int(sys.argv[3])
    seed = int(sys.argv[4])

    rng = np.random.RandomState(seed)

    characters = pd.read_csv(cfilename)
    task = pd.read_csv(tfilename)

    indices = rng.choice(characters.shape[0], size=count, replace=False)
    heroes = characters.iloc[indices].to_dict('records')
    enemies = task.to_dict('records')

    # print(indices)
    # print(heroes)
    # print(enemies)

    battle = Battle([Character(f'hero{i}', attr) for (i, attr) in enumerate(heroes)],
                    [Character(f'enemy{i}', attr) for (i, attr) in enumerate(enemies)],
                    rng)

    print(f'{battle.score()}')
