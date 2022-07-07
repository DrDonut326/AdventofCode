from collections import deque, defaultdict


def play_game(num_marbles, num_players):
    circle = deque([0])
    marble = 0
    players = defaultdict(int)
    current_player = 0
    while marble < num_marbles:
        # Increment players
        current_player += 1
        if current_player > num_players:
            current_player = 1

        # Inc current marble
        marble += 1

        # See if the current marble is div by 23
        if marble % 23 == 0:
            players[current_player] += marble
            circle.rotate(7)
            players[current_player] += circle.popleft()

        else:
            circle.rotate(-2)
            circle.appendleft(marble)

    return players


def get_high_score(scores):
    return max(scores.values())


def main():
    num_players = 447
    num_marbles = 71510
    scores = play_game(num_marbles, num_players)
    print(get_high_score(scores))  # Part 1 answer

    num_marbles *= 100
    scores = play_game(num_marbles, num_players)
    print(get_high_score(scores))  # Part 2 answer


main()
