import re

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

def recalculate_freqs(sample):
    c = [0 for i in chars]
    for w in sample:
        for i in range(26):
            if chars[i] in w:
                c[i] += 1
    return [i / len(sample) for i in c]
freqs = recalculate_freqs(words)

known_g = [None for i in range(5)]
known_b = [[] for i in range(5)]
known_present = []

def color_fmt(word):
    color_g = "\033[1;32m"
    color_y = "\033[1;33m"
    color_a = "\033[2;37m"
    color_u = "\033[0;36m"
    t = ""
    for i in range(5):
        if word[i] == known_g[i]:
            t += color_g
        elif word[i] in known_b[i]:
            t += color_a
        elif word[i] in known_present:
            t += color_y
        else:
            t += color_u
        t += word[i]
    t += "\033[0m"
    return t

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

ansi_escape_8bit = re.compile(
    br'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])'
)
def rankprint(word, data):
    cword = ansi_escape_8bit.sub(b'', bytes(word, "utf-8"))
    jword = (" " * (20 - len(cword))) + word
    print(jword + " | " + " | ".join([i.ljust(16) for i in data]))
def rankhead():
    rankprint("word", ["P(useful)", "P(win)", "P(finds info)"])
def rankfmt(w, r):
    rankprint(color_fmt(w), [str(int(p * 100)) + "%" for p in r])

while True:
    wp = gen_winning_possibilities()
    # freqs = recalculate_freqs(wp)
    # recalculating this every time will make it reflect the letter frequency of words that are *actually possible*
    # so that should work, i think
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
            known_present.append(word[i])
        elif colors[i] == "Y":
            known_b[i].append(word[i])
            known_present.append(word[i])
        elif colors[i] == "A":
            [known_b[j].append(word[i]) for j in range(5)]
    words.remove(word)


