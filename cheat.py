def pp(x):
    # pre-process
    x = x.upper()
    return x

def dedup(w):
    return "".join(set(w))

words = [pp(x) for x in open("words.txt").read().split("\n") if len(x) > 2]
# from wikipedia
chars = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
freqs = [0.127, 0.091, 0.082, 0.075, 0.07, 0.067, 0.063, 0.061, 0.06, 0.043, 0.04, 0.028, 0.028, 0.024, 0.024, 0.022, 0.02, 0.02, 0.019, 0.015, 0.0098, 0.0077, 0.0015, 0.0015, 0.00095, 0.00074]

known_g = [None for i in range(5)]
known_b = [[] for i in range(5)]

def gen_winning_possibilities():
    def f(x):
        for i in range(len(x)):
            if known_g[i] != None and x[i] != known_g[i]:
                return False
            if x[i] in known_b[i]:
                return False
        return True
    return list(filter(f, words))

def ranks(word, winning_possibilities):
    p_win = (1 / len(winning_possibilities)) if word in winning_possibilities else 0
    p_finds_info = 0
    for i in range(len(word)):
        if word[i] in word[:i]: continue
        if word[i] in known_b[i]: continue
        p_this_has_info = freqs[chars.index(word[i])]
        p_finds_info += (1 - p_finds_info) * p_this_has_info
    utility = p_win + (1 - p_win) * p_finds_info
    return (utility, p_win, p_finds_info)

def rankprint(word, data):
    print(word.rjust(20) + " | " + " | ".join([i.ljust(16) for i in data]))
def rankhead():
    rankprint("word", ["P(useful)", "P(win)", "P(finds info)"])
def rankfmt(w, r):
    rankprint(w, [str(int(p * 100)) + "%" for p in r])

while True:
    wp = gen_winning_possibilities()
    if len(wp) == 0:
        print("i give up!")
        break
    utilranked = sorted(words, key = lambda w: ranks(w, wp)[0], reverse = True)
    rankhead()
    for i in range(5):
        w = utilranked[i]
        r = ranks(w, wp)
        rankfmt(w, r)
    print("--- enter selected word, then colors ---")
    word = pp(input("> "))
    colors = pp(input("> "))
    if len(colors.replace("G", "")) == 0:
        print("--- YOU WIN!! ---")
        break
    for i in range(5):
        if colors[i] == "G":
            known_g[i] = word[i]
        elif colors[i] == "Y":
            known_b[i].append(word[i])
        elif colors[i] == "A":
            [known_b[j].append(word[i]) for j in range(5)]
    words.remove(word)


