# from collections import Counter


def merge(dict1, dict2):
    dict1.update(dict2)
    return dict1


dict1 = {"a": 1, "b": 2, "c": 3}
dict2 = {"a": 2, "c": 4, "d": 5}

merged_dict = merge(dict1, dict2)
print(merged_dict)
