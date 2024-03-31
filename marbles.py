import copy
import pprint

SOLUTIONS = []
# Memoize possibilities
BOARD_POSSIBILITIES = {}


def _neighbors(board, coords, char, directions=[(0, 1), (0, -1), (-1, 0), (1, 0)]):
    """
    Given a board and a set of coordinates, determine if the coordinate's neighbor in
    the given directions is char.
    """
    neighbors = []
    for direction in directions:
        neighbor_i = coords[0] + direction[0]
        neighbor_j = coords[1] + direction[1]
        try:
            if board[neighbor_i][neighbor_j] == char:
                neighbors.append((neighbor_i, neighbor_j, direction))
        except IndexError:
            continue
    return neighbors


def _gen_possible_moves(board):
    """Given a board, determine and return all possible moves."""
    board_str = "".join(str(item) for row in board for item in row)
    if board_str in BOARD_POSSIBILITIES:
        return BOARD_POSSIBILITIES[board_str]

    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "o":
                marble_neighbors = _neighbors(board, (i, j), "o")
                for marble_neighbor_i, marble_neighbor_j, direction in marble_neighbors:
                    open_neighbors = _neighbors(
                        board,
                        (marble_neighbor_i, marble_neighbor_j),
                        "_",
                        directions=[direction],
                    )
                    for open_neighbor_i, open_neighbor_j, _ in open_neighbors:
                        new_board = copy.deepcopy(board)
                        new_board[i][j] = "_"
                        new_board[marble_neighbor_i][marble_neighbor_j] = "_"
                        new_board[open_neighbor_i][open_neighbor_j] = "o"
                        moves.append(new_board)

    BOARD_POSSIBILITIES[board_str] = moves
    return moves


def starting_board():
    """Start the board with an empty space in the middle."""
    board = []
    board.append(list("xxoooxx"))
    board.append(list("xxoooxx"))
    board.append(["o"] * 7)
    board.append(list("ooo_ooo"))
    board.append(["o"] * 7)
    board.append(list("xxoooxx"))
    board.append(list("xxoooxx"))
    return board


def _solved(board):
    """Check for the case where the board has 1 marble left."""
    full = "".join(str(item) for row in board for item in row)
    return full.count("o") == 1


def recurse(moves):
    """
    If the last move taken results in 1 marble left, add the moveset to the list of
    solutions. If not, generate all possible moves off of the last move taken and
    recurse.
    """
    if _solved(moves[-1]):
        SOLUTIONS.append(moves)
        print("\n" * 5)
        print("SOLUTION")
        print("\n" * 5)
        pprint.pprint(moves)
        return

    possible_moves = _gen_possible_moves(moves[-1])
    for move in possible_moves:
        recurse(moves + [move])


def main():
    moves = [starting_board()]
    try:
        recurse(moves)
    except KeyboardInterrupt:
        print(f"Up until this point, {len(SOLUTIONS)} solutions found")


if __name__ == "__main__":
    main()
