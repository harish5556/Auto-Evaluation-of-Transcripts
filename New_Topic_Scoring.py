import gensim
import nltk
import warnings
import re
from nltk.corpus import wordnet
from pywsd.lesk import adapted_lesk
import spacy
import numpy as np
from gensim.models import LdaModel, LsiModel
from gensim.corpora import Dictionary
from PyDictionary import PyDictionary
warnings.filterwarnings('ignore')
dictionary = PyDictionary()


"""Compute similarity between two synsets
 synset1.wup_similarity(synset2): Wu-Palmer Similarity: Return a score denoting how similar two word senses are,
 based on the depth of the two senses in the taxonomy and that of their 
 Least Common Subsumer (most specific ancestor node)"""


def compute_similarity(synsets1, synsets2):
    score, count = 0.0, 0
    print(synsets1)
    print(synsets2)
    print("------------------")
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        samp_score = []
        # calculating similarity using wup_similarity
        best_score = [synset.wup_similarity(ss) for ss in synsets2]
        for i in best_score:
            if i is not None:
                samp_score.append(i)
        if len(samp_score) is not 0:
            new_best_score = max(samp_score)
            index = samp_score.index(max(samp_score))
            print(str(index) + " " + str(synsets2[index]))
        else:
            samp_score.append(0)
            new_best_score = max(samp_score)
        print(samp_score)
        # Check that the similarity could have been computed
        if new_best_score is not None:
            score += new_best_score
            count += 1
    # Average the values
    score /= count
    return score



# Getting topic from the text using Gensim LDA and LSI Topic Modeling Techniques. It also uses Spacy English model.
def get_topic(text):
    np.random.seed(100)
    nlp = spacy.load('en')
    my_stop_words = [u'say', u'\'s', u'Mr', u'be', u'said', u'says', u'saying', u'get']
    for stopword in my_stop_words:
        lexeme = nlp.vocab[stopword]
        lexeme.is_stop = True
    doc = nlp(text)
    article = []
    texts = []
    for w in doc:
        # if it's not a stop word or punctuation mark, add it to our article!
        if w.text != '\n' and not w.is_stop and not w.is_punct and not w.like_num:
            # we add the lematized version of the word
            article.append(w.lemma_)
    texts.append(article)
    # getting bigrams out of words using gensim
    bigram = gensim.models.Phrases(texts)
    texts = [bigram[line] for line in texts]
    # Creating corpus with our words
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(i) for i in texts]
    # Applying LDA and LSI models
    lsimodel = LsiModel(corpus=corpus, num_topics=10, id2word=dictionary)
    ldamodel = LdaModel(corpus=corpus, num_topics=10, id2word=dictionary)
    lsitopics = [[word for word, prob in topic] for topicid, topic in lsimodel.show_topics(formatted=False)]
    ldatopics = [[word for word, prob in topic] for topicid, topic in ldamodel.show_topics(formatted=False)]
    topics = []
    for i in ldatopics:
        topics.append(i[0])
    tags = nltk.pos_tag(topics)
    # removing verbs as generally nouns are topics
    lfinaltopics = [word for word, pos in tags if pos != 'VB' and pos != 'VBD' and pos != 'VBN' and pos != 'VBP' and pos != 'VBZ' and pos!='VBG' and pos != 'JJ' and pos != 'RB']
    ldafinaltopics = list(set(lfinaltopics))
    lstopics = []
    for i in lsitopics:
        for j in i:
            lstopics.append(j)
    ltags = nltk.pos_tag(lstopics)
    lsifinaltopics = [word for word,pos in ltags if pos != 'VB' and pos != 'VBD' and pos != 'VBN' and pos!= 'VBP' and pos!= 'VBZ' and pos!='VBG' and pos!= 'RB' and pos != 'JJ']

    # Intersection of results from both models
    finaltopics = list(set(ldafinaltopics) & set(lsifinaltopics))
    final_topics = []
    for i in finaltopics:
        if len(i) >= 2:
            final_topics.append(i)
    return final_topics


# It does all preprocessing for our answer and returns the clean text along with the topics in that text
def get_suggested_answer_topics():
    # Cleaning our text
    # demo1.txt has suggested answer
    que = open("demo1.txt", encoding = 'utf8').read().lstrip()
    que = re.sub(r'\s+', ' ', que)
    que_topics = get_topic(que)
    print("Suggested answer topics")
    print(que_topics)
    return que_topics, que


def get_student_answer_topics():
    # Cleaning our text
    # demo2.txt has student answer
    text = open("demo2.txt", encoding = "utf8").read().lstrip()
    text = re.sub(r'\s+', ' ', text)
    print(text)
    answer_topics = get_topic(text)
    print("student answer Topics")
    print(answer_topics)
    return answer_topics, text


def topic_match(que_topics, ans_topics, topic_match_length):
    # match_percent finds how many topics are matched with respect to question topics. This remains same for any case given below
    # If topics_matched = 4 and question topics= 6
    # match_percent= (4/6)*100 =  66.66
    match_percent = (topic_match_length / len(que_topics))*100
    # case 1: if the number of question topics and answer topics is same Ex: [1,2,3,4] [2,3,4,5]
    if len(que_topics) == len(ans_topics):
        #  sub case 1: all topics are matched in both topic lists
        if topic_match_length == len(que_topics):
            return 100
        #  sub case 2: less than 40 % topics are matched
        # Example : let question topics be [1,2,3,4]
        #           answer topics be [1,5,6,7]
        #            as we saw topic 1 is matched
        #            match_percent = 1/4 *100 = 25
        #            match_score = 25-(25*0.3)= 17.5 ( Penalising factor for irrelevancy is 0.3 )
        elif match_percent < 40:
            match_score = match_percent - (match_percent * 0.3)
        #  sub case 3: less than 50 % and >= 40 % topics are matched
        #               Penalising factor for irrelevancy is 0.25
        elif match_percent >= 40 & int(match_percent) < 50:
            match_score = match_percent - (match_percent * 0.25)
        # sub case 4 and 5 : >= 50 and < 70
        # question topics =[ 1,2,3,4,5,6]
        # answer topics =[1,2,3,4,7,8]
        # match_percent = 66
        # match_score= 66- ((100-66)*0.2) = 57.2
        # penalising factor for the above case is 0.2 of percentage of unmatched topics
        # for sub case 5 : penalising factor is 0.1
        elif match_percent >= 50 & int(match_percent) < 70:
            match_score = match_percent - ((100 - match_percent) * 0.2)
        else:
            match_score = match_percent - ((100 - match_percent) * 0.1)
        return match_score

    # Case:II   If number of suggested answer topics1 > student answer topics

    elif len(que_topics) > len(ans_topics):
        # irrelevancy = percent of irrelevant things written with respect to total student topics
        # sub case 1:
        # example : suggested topics (ST) = [1,2,3,4,5,6]
        # student topics (S2T) =[1,2,8,9]
        # match_percent= (2/6)*100 = 33
        # irrelevant_percent = (2/4)*100= 50
        # match_score = 33- 33(0.4)= 19.8
        if topic_match_length < len(ans_topics):
            irrelevant_topics = len(ans_topics) - topic_match_length
            irrelevant_percent = (irrelevant_topics / len(ans_topics)) * 100
            if irrelevant_percent >= 60:
                match_score = match_percent * 0.5
            elif irrelevant_percent < 60 & int(irrelevant_percent) >= 50:
                match_score = match_percent - match_percent * 0.4
            elif irrelevant_percent < 50 & int(irrelevant_percent) >= 40:
                match_score = match_percent - match_percent * 0.3
            else:
                match_score = match_percent - match_percent * 0.1
           # match_score = match_percent - match_percent * irrelevant_percent
        else:
            match_score = match_percent
        return match_score
    # Case 3: if number of ST <  S2T
    # Example ;
    # ST=[1,2,3,4]
    # S2T = [1,2,3,7,8,9]
    # match_percent = 3/4*100 =75
    # irrelevancy =  3/6*100 =50
    # irrelevancy = 50*0.3= 15
    # match_score = 75-15= 60
    else:
        irrelevancy = (len(ans_topics) - topic_match_length) / len(ans_topics) * 100
        if irrelevancy <= 30:
            irrelevancy = irrelevancy * 0.1
            match_score = match_percent - irrelevancy
        elif irrelevancy > 30 & int(irrelevancy) <= 40:
            irrelevancy = irrelevancy * 0.2
            match_score = match_percent - irrelevancy
        elif irrelevancy > 40 & int(irrelevancy) <= 50:
            irrelevancy = irrelevancy * 0.3
            match_score = match_percent - irrelevancy
        else:
            irrelevancy = irrelevancy * 0.4
            match_score = match_percent - irrelevancy
        return match_score


def get_similarity():
    que_topics, que = get_suggested_answer_topics()
    answer_topics, text = get_student_answer_topics()
    length = len(list(set(que_topics) & set(answer_topics)))
    print(str(length) + " topics matched")
    # Calculating the score based on number of topics matched
    topics_score = abs(topic_match(que_topics, answer_topics, length))
    print("")
    print(topics_score)
    synsets_que_topics = []
    synsets_ans_topics = []
    sim_score = 0
    # calculating similarity using wordnet's wup_similarity
    # Getting appropriate sense of topic from the text using "lesk"(word sense disambiguation algorithm)
    for i in que_topics:
        synsets_que_topics.append(adapted_lesk(que, i, pos='n'))
    for i in answer_topics:
        synset_answer = adapted_lesk(text, i, pos='n')
        print(str(synset_answer)+'..')
        if str(synset_answer) != "None":
            synsets_ans_topics.append(synset_answer)
    print("Similarity Score")
    sim_score = compute_similarity(synsets_que_topics, synsets_ans_topics) * 100
    print(sim_score)
    print("")
    print("Average Score: " + str(abs(topics_score + int(sim_score)/ 2)))

get_similarity()
