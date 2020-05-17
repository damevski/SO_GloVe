"""
preprocess-twitter.py

python preprocess-twitter.py "Some random text with #hashtags, @mentions and http://t.co/kdjfkdjf (links). :)"

Script for preprocessing tweets by Romain Paulus
with small modifications by Jeffrey Pennington
with translation to Python by Motoki Wu
with modifications for SO by Kosta Damevski

Translation of Ruby script to create features for GloVe vectors for Twitter data.
http://nlp.stanford.edu/projects/glove/preprocess-twitter.rb
"""

import re

FLAGS = re.MULTILINE | re.DOTALL


def camelcase(text):
    text = text.group()
    return text.lower() + " <camelcase> "

def allcaps(text):
    text = text.group()
    return text.lower() + " <allcaps> "

def methodcall(text):
    text = text.group(1)
    return text.lower() + " <methodcall> "

def tokenize(text):
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "<url>")
    text = re_sub(r"/"," / ")
    text = re_sub(r"@\w+", "<user>")
    # text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), "<smile>")
    # text = re_sub(r"{}{}p+".format(eyes, nose), "<lolface>")
    # text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), "<sadface>")
    # text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), "<neutralface>")
    text = re_sub(r" [-+]?[.\d]*[\d]+[:,.\d]*", " <number>")
    text = re_sub(r"([!?.]){2,}", r"\1 <repeat>")
    text = re_sub(r"([0-9A-Z]){2,} ", allcaps)
    text = re_sub(r"[A-Z]+[a-z0-9]+[A-Z]+\w* ", camelcase)
    text = re_sub(r"([a-zA-Z0-9-_]+)\(\) ", methodcall)
    text = re_sub(r"[\n:;,]", " ")
    text = re_sub(r"\. ", " . ")
    text = re_sub(r"\? ", " ? ")
    text = re_sub(r" \(", " ( ")
    text = re_sub(r"\) ", " ) ")

    return text.lower()


if __name__ == '__main__':
    text = "I JUnit aa_bb_cc aa-bb-cc RunTheWay TEST alllll foo() kinds of #hashtags and #HASHTAGS, @mentions and 3000 (http://t.co/dkfjkdf). w/ <3 :) haha!!!!!"
    tokens = tokenize(text)
    print(tokens)