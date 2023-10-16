from keyboard import Keyboard

qwerty = Keyboard(staggered=True)
print(round(qwerty.get_distance("rg"), 2), "rg", 1.6)
print(round(qwerty.get_distance("my"), 2), "my", 2.66)
print(round(qwerty.get_distance("vt"), 2), "vt", 2.02)
print(round(qwerty.get_distance("fg"), 2), "fg", 1)
print(round(qwerty.get_distance("fr"), 2), "fr", 1.03)
print(round(qwerty.get_distance("fv"), 2), "fv", 1.12)
print(round(qwerty.get_distance("vt"), 2), "vt/nu", 2.02)  # nu
print(round(qwerty.get_distance("ft"), 2), "ft", 1.25)
print(round(qwerty.get_distance("fb"), 2), "fb", 1.8)
print(round(qwerty.get_distance("jn"), 2), "jn", 1.12)
print(round(qwerty.get_distance("jy"), 2), "jy", 1.6)
print(round(qwerty.get_distance("mh"), 2), "mh", 1.8)
print(round(qwerty.get_distance("rg"), 2), "rg", 1.6)
print(round(qwerty.get_distance("i."), 2), "i.", 0)
