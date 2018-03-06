#This Class is going to take paragraphs and return whether given statement can return a parse tree or not
import time
import nltk
import re
from nltk import word_tokenize
import Grammar
import Constants
class ParseTree:
    def init(self):
        print("Starting the Grammar Check")
        self.startTime=time.time()
        self.grammar=nltk.CFG.fromstring(Grammar.grammar)
        self.caps = Constants.caps
        self.prefixes = Constants.prefixes
        self.suffixes = Constants.suffixes
        self.starters = Constants.starters
        self.acronyms = Constants.acronyms
        self.websites = Constants.websites
        self.run()

    def run(self):
        self.sent = open("demo.txt").readlines()
        self.sent = ''.join(self.sent)
        self.sent = self.split_into_sentences(self.sent)
        self.validateSentence()

    def splitIntoSentences(self,text):
        """This function is going to split the text into sentences
            input: raw text
            output: List of sentences
        """
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(self.prefixes, "\\1<prd>", text)
        text = re.sub(self.websites, "<prd>\\1", text)
        if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + self.caps + "[.] ", " \\1<prd> ", text)
        text = re.sub(self.acronyms + " " + self.starters, "\\1<stop> \\2", text)
        text = re.sub(self.caps + "[.]" + self.caps + "[.]" + self.caps + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(self.caps + "[.]" + self.caps + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" " + self.suffixes + "[.] " + self.starters, " \\1<stop> \\2", text)
        text = re.sub(" " + self.suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(" " + self.caps + "[.]", " \\1<prd>", text)
        if "”" in text: text = text.replace(".”", "”.")
        if "\"" in text: text = text.replace(".\"", "\".")
        if "!" in text: text = text.replace("!\"", "\"!")
        if "?" in text: text = text.replace("?\"", "\"?")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences

    def validateSentence(self):
        """This function is going to split the sentences into words,applies pos tagging, extract tags and generates
            parse trees using the tags
            input: List of sentences
            output: returns validity of sentences
         """
        for s in self.sent:
            count = 0
            s = "".join(c for c in s if c not in ('!', '.', ':', ','))
            stoken = word_tokenize(s)
            # print(stoken)
            tagged = nltk.pos_tag(stoken)
            pos_tags = [pos for (token, pos) in nltk.pos_tag(stoken)]
            # print(pos_tags)
            rd_parser = nltk.LeftCornerChartParser(self.grammar)
            for tree in rd_parser.parse(pos_tags):
                count = count + 1
                break
            if count == 0:
                print("Invalid sentence")
            else:
                print("Valid sentence")
        print("Total time taken:",(time.time()-self.startTime))

    if __name__=="__main__":
       init()
