from functions.data_in import read_data


def format_data(file_path='input.txt'):
    data = read_data(file_path)
    player1 = int(data[0].split(': ')[1])
    player2 = int(data[1].split(': ')[1])
    return player1, player2


class Die:
    def __init__(self):
        self.rolls = 0

    @property
    def three_roll_sum(self):
        result = self.rolls * 3 + 6
        self.rolls += 3
        return result


class AllWorldsFinished(Exception):
    pass


class QuantumDie(Die):
    effective_values = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    state = list()

    def __init__(self):
        super(QuantumDie, self).__init__()
        self.counts = 1

    @property
    def three_roll_sum(self):
        if self.rolls >= len(self.state):
            result = 3
            self.state.append(result)
        else:
            result = self.state[self.rolls]
        self.rolls += 1
        self.counts *= self.effective_values[result]
        return result

    @classmethod
    def increase_state(cls):
        for idx, value in enumerate(cls.state[::-1]):
            if value == 9:
                continue
            cls.state = cls.state[:-idx - 1] + [cls.state[-idx - 1] + 1]
            return
        raise AllWorldsFinished('Done')


class Player:
    win_value = 1000

    def __init__(self, position):
        self.score = 0
        self.position = position

    def move(self, steps):
        self.position = (self.position - 1 + steps) % 10 + 1
        self.score += self.position

    def won(self):
        return self.score >= Player.win_value


class Game:
    die_class = Die

    def __init__(self, pos1, pos2):
        self.player1 = Player(pos1)
        self.player2 = Player(pos2)
        self.die = Game.die_class()

    def play(self):
        to_move, other = self.player1, self.player2
        while True:
            to_move.move(self.die.three_roll_sum)
            if to_move.won():
                break
            to_move, other = other, to_move


def part_one():
    game = Game(*format_data())
    game.play()
    loosing_player = game.player1 if game.player2.won() else game.player2
    print(game.die.rolls)
    print(loosing_player.score * game.die.rolls)


def part_two():
    start_values = format_data()
    Game.die_class = QuantumDie
    Player.win_value = 21
    wins = [0, 0]
    while True:
        try:
            game = Game(*start_values)
            game.play()
            wins[int(game.player2.won())] += game.die.counts
            QuantumDie.increase_state()
        except AllWorldsFinished as e:
            break
    print(max(wins))


if __name__ == '__main__':
    part_one()
    part_two()
