#Import Library Files
import sys
import nltk
import operator
from nltk.tokenize import word_tokenize
from nltk.corpus import brown

def load_dict():
    category_noun_dictionary = {}
    
    br_cats=['adventure', 'fiction', 'mystery', 'reviews', 'science_fiction']
    #Finding top 500 words from categories
    for category in br_cats:
        top_words_category=[]
        words_of_category = brown.words(categories=category)
        category_word_freq = nltk.FreqDist(w.lower() for w in words_of_category)
        top_in_category = category_word_freq.most_common(500)
        for i in top_in_category:
            top_words_category.append(i[0])
        top_words_category = set(top_words_category)
        category_noun_dictionary[str(category)] = top_words_category

    #Get top 500 words from Programming Language
    reload(sys)  
    sys.setdefaultencoding('Cp1252')
    plfile = open("PL_corpora.txt").read()
    pl_top=[]
    plwords=word_tokenize(plfile);
    pl_freq = nltk.FreqDist(w.lower() for w in plwords)
    pl_topf=pl_freq.most_common(500)
    for i in pl_topf:
       pl_top.append(i[0])
    pl_top = set(pl_top)
    category_noun_dictionary['programming_language'] = pl_top
    
    return category_noun_dictionary


def classify_file(filename,category_noun_dictionary):
    
    reload(sys)  
    sys.setdefaultencoding('Cp1252')
    
    #Read input file
    inpfile = open(filename).read()

    #Tokenize
    inpwords=word_tokenize(inpfile);

    #POS
    tagged=nltk.pos_tag(inpwords)

    #Extracting Nouns using Chunking
    chunkGram = r"""Chunk: {<NN.?.?>}"""
    chunkParser = nltk.RegexpParser(chunkGram)

    #Get Parse Tree
    chunked = chunkParser.parse(tagged)

    #Initialise
    inpfinal=[]
    content_top=[]

    features_dict={}

    #Append Nouns to Array
    for subtree in chunked.subtrees():
       if subtree.label() == 'Chunk':
            inpfinal.append(subtree[0][0])

    #Frequency Distribution
    freqn = nltk.FreqDist(w.lower() for w in inpfinal)

    #Get top 500 words from Content
    content_topf=freqn.most_common(500)
    for i in content_topf:
        content_top.append(i[0])

    #Searching
    for category in category_noun_dictionary.keys() :
        count=0
        for i in content_top:
            if i in category_noun_dictionary[category] :
                count+=1
        features_dict[category]= count

    default=10 #Threshold value
    features_dict['Other']= default

    #Print File Name
    print ("Processing: " + filename)

    #Get MAX of count from dictionary of counts
    maxkey=max(features_dict.iteritems(), key=operator.itemgetter(1))[0]
    print "Matched "+str(features_dict[maxkey])+" words with category "+maxkey
    return maxkey