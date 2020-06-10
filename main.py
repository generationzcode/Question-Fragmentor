from flask import Flask, render_template, request,url_for
import nltk
from nltk.tokenize import PunktSentenceTokenizer
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
def tokenizeText(text):
  text = text.replace("?","?,")
  custom_sent_tokenizer = PunktSentenceTokenizer(text)
  tokenize = custom_sent_tokenizer.tokenize(text)
  return tokenize
def process_content(tokenized,text):
    text = text.replace("?","?,")
    for i in tokenized:
            arr = []
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""seperator: {<CC.?>*|<UH.?>*|<,.?>*|<IN.?>*}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            arr=[]
            wordPos=0
            wordLen=0
            for subtrees in chunked.subtrees():
                    arr1=[]
                    for subtree in subtrees:
                        if(type(subtree) is nltk.tree.Tree):
                          pop=''
                          try:
                            pop = arr1[-1]
                          except:
                            pop=''
                          arr.append(" ".join(arr1))
                          wordPos = text.find(pop)
                          wordLen = len(pop)
                          arr1=[]
                        else:
                            arr1.append(subtree[0])
            arr.append(text[wordPos+wordLen:-1]+text[-1])
            return arr

web_site = Flask(__name__)

@web_site.route('/')
def index():
	return render_template('index.html')
@web_site.route('/results', methods=['POST', 'GET'])
def results():
  text = process_content(tokenizeText(request.form["sampletext"]),request.form["sampletext"])
  return render_template('results.html',text=text)


web_site.run('0.0.0.0',8080)