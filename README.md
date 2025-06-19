This tool lets you cheat at Wordle!
You probably shouldn't actually use it to cheat, because that is not cool.
However, the task of finding the best word to play is a very interesting problem, which is why I made the tool.

# How to use

The tool is very simple.
It tells you a list of the top 5 guesses, arranged by a synthetic metric called "utility".
Choose whichever one of those you want (the top one is generally the best guess).
Then play that word in Wordle.
You can also choose a different word, if you don't like the ones it gives you.
For instance, if you think you have a better opener, you can just play that.

Once you've played it, you type in the word you played, and press enter.
Then, you must encode the color data.

Use this key:

- Green = G
- Yellow = Y
- Gray = A

Suppose you play the word "CUBES".
Suppose further that "C" and "B" are yellow, "U" is green, and the rest are gray.
Then the color encoding would be "YGYAA".

Once you've entered both the word you played and the resulting colors, the tool will perform some math and deliver new guesses.
Repeat until you beat the game!

# How it works

While the tool's code seems quite crazy and messy, the algorithm is really quite simple.

Let's start with the three metrics.

## The "win" metric

The "win" metric gives you an idea of the probability that this word is the winning word. It is by far the most simple formula: P(win) = (number of words that might win)^{-1}. This formula works because we assume that every word has an equivalent probability of being chosen.

## The "finds info" metric

The "finds info" metric gives you an idea of the probability that this word finds a character that is in the word we're trying to guess. Essentially, P(this character finds information in the word) = (1 - P(information has already been found)) * P(this character contains information). Of course, we discern the likelihood that the character is in the unknown word by using frequency analsis.

## The "utility" metric

The utility metric is a representation of how likely this word is to be useful. It is the sum of the probabilty that a win occurs and the probability that we find information but don't win.

We assume that P(win) and P(find info) are independent. This makes the formula much more tiny and efficient. Thus P(useful) = P(win) + (1 - P(win)) * P(find info).

# Example playthrough

Here's an example playthrough using the tool to guess the word "prune".
You can reproduce it by playing a game at [this](https://www.wordle.name/en/) Wordle emulator.

```
% python3 cheat.py
                word | P(useful)        | P(win)           | P(finds info)
               AEROS | 90%              | 0%               | 90%
               AROSE | 90%              | 0%               | 90%
               SOARE | 90%              | 0%               | 90%
               ARISE | 90%              | 0%               | 90%
               RAISE | 90%              | 0%               | 90%
--- enter selected word, then colors ---
> AEROS
> AYYAA
                word | P(useful)        | P(win)           | P(finds info)
               LITER | 82%              | 0%               | 82%
               LITRE | 82%              | 0%               | 82%
               TILER | 82%              | 0%               | 82%
               LINER | 82%              | 0%               | 82%
               INERT | 82%              | 0%               | 82%
--- enter selected word, then colors ---
> LITER
> AAAYY
                word | P(useful)        | P(win)           | P(finds info)
               PRUNE | 78%              | 0%               | 78%
               RUNCE | 78%              | 0%               | 78%
               CRYNE | 77%              | 0%               | 77%
               DRUPE | 77%              | 0%               | 77%
               PRUDE | 77%              | 0%               | 77%
--- enter selected word, then colors ---
> PRUNE
> GGGGG
--- YOU WIN!! ---
```

# Credits

Thanks to `dracos` for the [word list](https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw/6bfa15d263d6d5b63840a8e5b64e04b382fdb079/valid-wordle-words.txt).

