import fasttext

def spredicter(text):
    model = fasttext.load_model("Sentiment.bin")
    labels, prob = model.predict(text)
    return labels[0][9:].capitalize().replace('_',' ')

def opredicter(text):
    model = fasttext.load_model("Offensive.bin")
    labels, prob = model.predict(text)
    if labels[0][9:] == 'yes':
        return 'Offensive'
    else:
        return 'Not offensive'

def rpredicter(text):
    model = fasttext.load_model("Relevant.bin")
    labels, prob = model.predict(text)
    if labels[0][9:] == 'yes':
        return 'Relevant'
    else:
        return 'Not relevant'