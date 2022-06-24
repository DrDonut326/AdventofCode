from Utility import get_input




class Dance:
    def __init__(self):
        self.positions = self.line_up()

    def line_up(self):
        letters = 'abcdefghijklmnop'
        letters = list(letters)
        return letters

    def spin(self, x):
        self.positions = self.positions[-x:] + self.positions[:-x]

    def exchange(self, a, b):
        self.positions[a], self.positions[b] = self.positions[b], self.positions[a]

    def partner(self, a, b):
        a_i = self.positions.index(a)
        b_i = self.positions.index(b)
        self.positions[a_i], self.positions[b_i] = self.positions[b_i], self.positions[a_i]

    def do_dance(self, move):
        if move[0] == 's':
            self.spin(int(move[1:]))
        elif move[0] == 'x':
            a, b = move[1:].split('/')
            self.exchange(int(a), int(b))
        elif move[0] == 'p':
            a, b = move[1:].split('/')
            self.partner(a, b)

    def get_dance_string(self):
        return ''.join(self.positions)

def main():
    dance_moves = get_input('line', do_split=True, split_key=',')[0]
    dance = Dance()
    resets = []
    for n in range(16):  # Change to a bigish number to get some data
        for move in dance_moves:
            dance.do_dance(move)
            if dance.get_dance_string() == 'abcdefghijklmnop':
                resets.append(n)
    for a, b in zip(resets, resets[1:]):
        print(b - a)  # Period of the dance

    # Divide 1 billion by the remainder // Find the remaining dances need to be done
    print(dance.get_dance_string())



main()
