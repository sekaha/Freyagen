from itertools import product

# generate all quadrigrams containing the swaps
chars = "abcdefghijklmnopqrstuvwxyz,./;"
swaps = ["a", "b"]
perm = ["" for _ in range(3)]


def helper(swap, chars, d, offset):
    d -= 1

    if d < 0:
        # Where I would process the delta
        res = perm[:offset] + [swap] + perm[offset:]
        print(res)
        return
    else:
        if d < offset:
            chars = chars.replace(swap, "")

        for c in chars:
            perm[d] = c
            helper(swap, chars, d, offset)


for swap in swaps:
    new_chars = chars

    for offset in range(4):
        helper(swap, new_chars, 3, offset)
    new_chars.replace(swap, "")


"""
perms = set()
for p in product(chars, repeat=4):
    if swaps[0] in p or swaps[1] in p:
        perms.add("".join(p))

print(len(perms))
"""
# print(perms - my_perms)
