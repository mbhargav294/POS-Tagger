#!/usr/bin/env python

from optparse import OptionParser
import os, logging, collections, math
import utils, re
import numpy as np

def create_model(sentences):
    model = None
    ## YOUR CODE GOES HERE: create a model
    tagCount = collections.defaultdict(float)
    wordList = collections.defaultdict(float)
    tagCountBigram = collections.defaultdict(lambda: collections.defaultdict(float))
    tagCountTrigram = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(float)))
    tagProbBigram = collections.defaultdict(lambda: collections.defaultdict(float))
    tagProbTrigram = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(float)))
    wordTagCount = collections.defaultdict(lambda: collections.defaultdict(float))
    wordTagProb = collections.defaultdict(lambda: collections.defaultdict(float))

    for sentence in sentences:
        for i in range(len(sentence)):
                wordTagCount[sentence[i].word][sentence[i].tag] += 1.0
                tagCount[sentence[i].tag] += 1.0
                wordList[sentence[i].word] += 1.0

    for sentence in sentences:
        for i in range(len(sentence)):
            if i < len(sentence) - 1:
                tagCountBigram[sentence[i].tag][sentence[i+1].tag] += 1.0
                
    for sentence in sentences:
        for i in range(len(sentence)):
            if i < len(sentence) - 2:
                tagCountTrigram[sentence[i].tag][sentence[i+1].tag][sentence[i+2].tag] += 1.0

    for key1, value1 in wordTagCount.iteritems():
        for key2, value2 in value1.iteritems():
            wordTagProb[key1][key2] = wordTagCount[key1][key2]/tagCount[key2]

    noTags = len(tagCount)
    for key1, value1 in tagCountBigram.iteritems():
        for key2, value2 in value1.iteritems():
            tagProbBigram[key1][key2] = (tagCountBigram[key1][key2]+1)/(tagCount[key1] + len(tagCount))
            
    for key1, value1 in tagCountTrigram.iteritems():
        for key2, value2 in value1.iteritems():
            for key3, value3 in value1.iteritems():
                tagProbTrigram[key1][key2][key3] = (tagCountTrigram[key1][key2][key3]+1)/(tagCountBigram[key1][key2] + noTags)

#    for key1, value1 in tagCount.iteritems():
#        for key2, value2 in tagCount.iteritems():
#            print '<s>', key1, key2, tagProbTrigram['<s>'][key1][key2]
    
    model = [tagCount, tagProbBigram, wordTagProb, wordList, tagProbTrigram]
    print "Training Completed"
    return model

def predict_tags(sentences, model):
    ## YOU CODE GOES HERE: use the model to predict tags for sentences
    tagCount = model[0]
    tagProbBigram = model[1]
    wordTagProb = model[2]
    wordList = model[3]
    tagProbTrigram = model[4]
    
    toWords = ['to']
    articleWords = ['the', 'a', 'an']
    dollarWords = ['$']
    dotWords = ['.', '?']

    tagIndex = []
    for key in tagCount:
        if key == '<s>':
            continue
        tagIndex.append(key)
    
    abc = 1
    for sentence in sentences:
        #print abc
        #abc += 1
        #if abc == 50:
        #    break
        Viterbi = [{}]
        for i in range(2, len(sentence)):
            word = sentence[i].word
            if not word in wordList:
                matched = 0
                hash = re.match('^#.*',word)
                user = re.match('^@.*',word)
                nums = re.match('.*[0-9].*',word)
                urls = re.match('(^http.*)|(^www.*)',word)
                emoticon = re.match(':.',word)
                proper = re.match('^[A-Z].*',word)
                #special = re.match('\W',word)
                if hash != None:
                    wordTagProb[word]['#'] = 1/tagCount['#']
                    matched = 1
                if user != None:
                    wordTagProb[word]['@'] = 1/tagCount['@']
                    matched = 1
                if nums != None:
                    wordTagProb[word]['$'] = 1/tagCount['$']
                    matched = 1
                if urls != None:
                    wordTagProb[word]['U'] = 1/tagCount['U']
                    matched = 1
                if emoticon != None:
                    wordTagProb[word]['E'] = 1/tagCount['E']
                    matched = 1
                if proper != None:
                    wordTagProb[word]['^'] = 1/tagCount['^']
                    matched = 1
                #if special != None:
                #    wordTagProb[word][','] = 1/tagCount['#']
                #    matched = 1
                if matched == 0:
                    wordTagProb[word]['N'] = 1 * 1/tagCount['N']
            if i == 2:
                for key in tagIndex:
                    wordProb = wordTagProb[word][key]
                    prevBigram = tagProbTrigram['<s>']['<s>'][key]
                    #print "hello", key
                    #Viterbi[i-2][key] = {"Prob": wordProb * prevBigram, "Prev1": None, "Prev2": None}
                    Viterbi[i-2][key] = {"Prob": wordProb * prevBigram, "Prev": None}
                    #print Viterbi[i-1][key]
            elif i == 3:
                Viterbi.append({})
                for key in tagIndex:
                    max_val = 0
                    max_val = max(Viterbi[i-3][key1]["Prob"] * tagProbTrigram['<s>'][key1][key] for key1 in tagIndex)
                    for key1 in tagIndex:
                        if max_val == Viterbi[i-3][key1]["Prob"] * tagProbTrigram['<s>'][key1][key]:
                            #Viterbi[i-2][key] = {"Prob": max_val * wordTagProb[word][key], "Prev1": None, "Prev2": key1}
                            Viterbi[i-2][key] = {"Prob": max_val * wordTagProb[word][key], "Prev": key1}
                            break
                    #print Viterbi[i-1][key]
                #print "Hello"
            else:
                Viterbi.append({})
                for key in tagIndex:
                    max_val = 0
                    fKey = 'N'
                    for key1 in tagIndex:
                        max_val1 = max(Viterbi[i-4][key1]["Prob"] * Viterbi[i-3][key2]["Prob"] * tagProbTrigram[key1][key2][key] for key2 in tagIndex)
                        if max_val1 > max_val:
                            #print key1, key, max_val1
                            max_val = max_val1
                            fKey = key1
                            
                    #print fKey
                    #for key1 in tagIndex:
                    for key2 in tagIndex:
                        if max_val == Viterbi[i-4][fKey]["Prob"] * Viterbi[i-3][key2]["Prob"] * tagProbTrigram[fKey][key2][key]:
                            max_val *= 10000
                            #if max_val != 0:
                            #    print key, fKey, key2, max_val
                            Viterbi[i-2][key] = {"Prob": max_val * wordTagProb[word][key], "Prev": key2}
                            break
        prev_tag = None
        for i in range(len(sentence)-1, 1, -1):
            #print sentence[i]
            word = sentence[i].word
            max_prob = 0
            max_prev = None
            if i == len(sentence)-1:
                #print sentence[i]
                for key,val in Viterbi[i-2].iteritems():
                    if val["Prob"] >= max_prob:
                        max_prob = val["Prob"]
                        max_prev = val["Prev"]
                        max_curr = key
                #print sentence[i]
                sentence[i].tag = max_curr
                prev_tag = max_prev
                #print sentence[i]
            else:
                #if word in toWords:
                #    sentence[i].tag = "TO"
                #elif word in articleWords:
                #    sentence[i].tag = "DT"
                #elif word in dollarWords:
                #    sentence[i].tag = "$"
                #elif word in dotWords:
                #    sentence[i].tag = "."
                #else:
                #print sentence[i]
                sentence[i].tag = prev_tag
                #print sentence[i]
                prev_tag = Viterbi[i-2][prev_tag]["Prev"]
    return sentences

if __name__ == "__main__":
    usage = "usage: %prog [options] GOLD TEST"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    training_file = args[0]
    training_sents = utils.read_tokens(training_file)
    test_file = args[1]
    test_sents = utils.read_tokens(test_file)

    model = create_model(training_sents)

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(training_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(training_sents, predictions)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(test_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(test_sents, predictions)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)
