from .search import search


def think(board):
    return search(board, depth=3)
