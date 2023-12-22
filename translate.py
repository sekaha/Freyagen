eao = "'ldwfzbu,yortschneaikxmgvpq-.j"

qwerty = "qwertyuiopasdfghjkl;zxcvbnm,./"

qwertytoeao = str.maketrans(eao + '"', qwerty + "Q")
eaotoqwerty = str.maketrans(qwerty + "Q", eao + '"')

s = """Currently looking at keycaps with rei..
I've looked through a lot but I think imma go with one of these two
idk why the images are so crispy
they're so foam gummy coded
They are
Foam moment
gummy shakr moment tbh
I'm thinking of throwing it on this base
it's important to me to have the key numbers tbh....
might also go with this one
they're pretty similar, this one just has foldable legs 
I also kinda wanted this but
I can't findk ey caps that would go well on it"""

# print("kel yiafi xd;es flj zihwkn ;vkd kel clbq n;m".translate(tb))
print(s.lower().translate(qwertytoeao))
