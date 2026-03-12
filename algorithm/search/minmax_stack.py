# 再帰を使わずにstackで書いたminmax法
# 再帰の方が優れているので使わない


# def minimax(board, max_depth, evaluate):

#     stack = [
#         {
#             "depth": 0,
#             "maximizing": not board.turn,
#             "moves": list(board.legal_moves),
#             "index": 0,  # 次に探索する子ノードのインデックス
#             "value": -float("inf")
#             if not board.turn
#             else float("inf"),  # 現局面の評価値
#             "best_moves": [],  # 現局面の最善手
#         }
#     ]

#     values = {}

#     while stack:
#         node = stack[-1]
#         depth = node["depth"]
#         maximizing = node["maximizing"]

#         key = board.zobrist_hash()

#         # 終端ノード
#         if depth == max_depth or board.is_game_over():
#             val = evaluate(board)
#             values[key] = val

#             stack.pop()

#             if stack:
#                 board.pop()

#                 parent = stack[-1]

#                 # 親ノードの評価値、最善手を更新
#                 if parent["maximizing"]:
#                     if val > parent["value"]:
#                         parent["value"] = val
#                         parent["best_moves"] = [parent["moves"][parent["index"] - 1]]
#                     elif val == parent["value"]:
#                         parent["best_moves"].append(
#                             parent["moves"][parent["index"] - 1]
#                         )

#                 else:
#                     if val < parent["value"]:
#                         parent["value"] = val
#                         parent["best_moves"] = [parent["moves"][parent["index"] - 1]]
#                     elif val == parent["value"]:
#                         parent["best_moves"].append(
#                             parent["moves"][parent["index"] - 1]
#                         )

#             continue

#         # 子ノードが残っている場合
#         if node["index"] < len(node["moves"]):
#             move = node["moves"][node["index"]]
#             node["index"] += 1

#             board.push(move)

#             stack.append(
#                 {
#                     "depth": depth + 1,
#                     "maximizing": not maximizing,
#                     "moves": list(board.legal_moves),
#                     "index": 0,
#                     "value": -float("inf") if not maximizing else float("inf"),
#                     "best_moves": [],
#                 }
#             )

#         # 子ノードの探索終了後
#         else:
#             val = node["value"]

#             stack.pop()

#             if stack:
#                 board.pop()

#                 parent = stack[-1]

#                 move = parent["moves"][parent["index"] - 1]

#                 if parent["maximizing"]:
#                     if val > parent["value"]:
#                         parent["value"] = val
#                         parent["best_moves"] = [move]
#                     elif val == parent["value"]:
#                         parent["best_moves"].append(move)

#                 else:
#                     if val < parent["value"]:
#                         parent["value"] = val
#                         parent["best_moves"] = [move]
#                     elif val == parent["value"]:
#                         parent["best_moves"].append(move)

#     return node["value"], node["best_moves"]
