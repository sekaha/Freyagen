# from collections import

chars = "abcdefghijklmnopqrstuvwxyz,.'-"
swaps = "abc"

checked_combos = set("".join(sorted(c + s)) for s in swaps for c in chars if s != c)

print(sorted(checked_combos))

# get ordered unique key combinations


# def merge(dict1, dict2):
#     dict1.update(dict2)
#     return dict1
#
#
# dict1 = {"a": 1, "b": 2, "c": 3}
# dict2 = {"a": 2, "c": 4, "d": 5}
#
# merged_dict = merge(dict1, dict2)
# print(merged_dict)
