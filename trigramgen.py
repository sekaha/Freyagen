from corpus import get_grams

valid = "qwertyuiopasdfghjklzxcvbnm,.-'"

trigrams = get_grams("res/trigrams.txt", valid)

total = sum(trigrams.values())
target_am = 0.98773  # this results in the number of possible permutations created by 30 chars, 30 chars, and 2 swaps... just a nice amount
target = target_am * total

# print(total)
trigram_count = 0
seen = 0

for i, v in enumerate(trigrams.values()):
    if seen >= target:
        print(i)
        break
    seen += v
    trigram_count += 1

print(target)
# print(trigram_count)
print(len(trigrams))
