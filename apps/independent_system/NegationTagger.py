# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from printHelper import Log

# from keras.models import Sequential
# from keras.layers import Dense
import OpinionsDatabase as db 
import os, random, json, io



tmp = os.popen('stty size', 'r').read().split()
WIDTH = int(tmp[1])-15 if tmp else 100

log = Log("./log")



sources = [
    "corpus_apps_android",
    "corpus_cine",
    "corpus_hoteles",
    "corpus_prensa_uy",
    "corpus_tweets",
    "corpus_tweets_2",
    "corpus_variado_sfu"
]



# class Network:
#     
#     def __init__(self,
#             hidden_layers=2,
#             activation=['relu'],
#             loss='binary_crossentropy', 
#             optimizer='adam', 
#             metrics=['accuracy']
#         ):
#         left = hidden_layers - len(activation)
#         for _ in range(left):
#             activation.append(activation[0]) 
#         self.model = Sequential()
#         self.model.add( Dense( 12, input_dim=8, activation=activation[0] ) )
#         for i in range(hidden_layers):
#             self.model.add( Dense( 8, activation=activation[i+1] ) )
#         self.model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
#     
#     def fit(self,X,Y):
#         self.model.fit(X, Y, epochs=150, batch_size=10)
#         scores = model.evaluate(X, Y)
#         for i in range(len(scores)):
#             print "\n%s: %.2f%%" % (model.metrics_names[i], scores[i]*100)
#         
#     def predict(self,X):
#         return self.model.predict(X)



def start_tagging():
    
    def DisplayMenu():
        os.system('clear')
        print "*"*20," MENU ","*"*20
        print "0 . exit"
        for i,source in enumerate(sources):
            print i+1,".",source
        return 
     
    def DisplayReview(_id,current,total,words,tags):
        os.system('clear')
        print "Review [%s]" % _id
        print "<<",
        for i in range(total):
            if i < current and tags[i] == 'n':
                print words[i]+"\033[93m/"+tags[i]+"\033[0m",
            elif i < current:
                print words[i]+"\033[91m/"+tags[i]+"\033[0m",
            elif i > current:
                print words[i]+"  ",
            else:
                print "\033[92m\033[4m"+words[i]+"\033[0m\033[0m  ",
        print ">>"
        
    def chunkstring(string, length):
        return (string[0+i:length+i] for i in range(0, len(string), length))
    
    def DisplayAnnotated(result,width=WIDTH):
        width = width-10
        row   = "%-7s | %-"+str(width)+"s"
        line  = "%-7s-+-%-"+str(width)+"s"
        print row% ("ID","ANNOTATION")
        print line % ("-"*7,"-"*width)
        for item in result:
            chunks = chunkstring(item['annotation'], width)
            chunks = list(chunks)
            print row % (str(item['id']),chunks[0])
            for chunk in chunks[1:]:
                print row % ("",chunk)
            print line % ("-"*7,"-"*width)
    
    def ViewSave(result):
        os.system('clear')
        op = raw_input("Done! View result? (y/n) > ")
        # Ask for display
        if op.lower() == 'y':
            DisplayAnnotated(result)
        # Ask for save in two steps
        op = raw_input("\nSave result? [y/n] > ")
        if op.lower() == 'n':
            op = raw_input("Are you sure? [y/n] > ")
            if op.lower() == 'y':
                return
        # Save the result
        db.save_negations(result)
        
    
    while True:
        # Display menu options
        DisplayMenu()
        op = raw_input("\nOption > ")
        if not op.isdigit() or int(op) > len(sources):
            raw_input("Opcion invalida")
            continue
        op = int(op)
        if op == 0:
            # Exit
            break
        else:    
            result,id = [],0        
            try:     
                # Ask for retrieving options 
                source = sources[op-1]
                op = raw_input("\nInsert indexes separated by ',' or <intro> for pick up randomly > ")
                if op: # From indexes
                    indexes = list(set(int(i) for i in op.split(',')))
                    quantity = len(indexes)
                    indexes = indexes[:quantity]
                else: # Randomly
                    while not op.isdigit():
                        op = raw_input("How many? > ")
                    quantity = int(op)
                    indexes = []
                
                # Get a sample of reviews from options
                samples = db.get_sample(quantity,source,indexes)
                
                # Tag every review
                left = quantity
                while left != 0:   
                                     
                    # Retrieve relevant data from the sample
                    sample  = samples[left-1]
                    _id     = sample['_id']
                    review  = sample['text']
                    
                    # Initialization (keep current words and empty categories)
                    words = [item['word'] for item in review]
                    total = len(words)
                    tags  = ['  ' for _ in range(total)]
                    
                    # For each word, annotate with (N) or (I) and give the possibility of back by pressing (B)
                    cat = ""
                    idx = 0
                    while True:
                        # Display review
                        DisplayReview(_id,idx,total,words,tags)
                        
                        # Check end condition
                        if idx == total:
                            op = raw_input("\nDone. Proceed with the next review (left %i)? [y/n] > " % (left-1))
                            if op == 'y':
                                break
                            idx = idx - 1 if idx != 0 else 0
                            tags[idx] = '  '
                            continue
                        
                        # Ask for input
                        tooltip  = "\nTag with N(ormal) or I(nverted). "
                        tooltip += "Enter A(bort), B(ack) or <intro> for "
                        tooltip += "repeating last action (%s) > " % (cat.upper() if cat else "None")
                        tag = raw_input(tooltip)
                        
                        if not tag and not cat: # Prevents parse empty cat
                            print "Input a category first";raw_input()
                            continue
                        elif tag:
                            cat = tag
                        
                        # Action from decision
                        cat = cat.lower()
                        if not cat or cat not in 'niba':
                            print "Option",cat,"is not correct." ;raw_input()
                            continue
                        if cat == 'b': # Back
                            idx = idx - 1 if idx != 0 else 0
                            tags[idx] = '  '
                        elif cat == 'a':
                            op = raw_input("Are you sure you want to abort (left %i)? [y/n] > " % left)
                            if op.lower() == 'y': raise Exception("Abort")
                        else:
                            # Associate the category
                            tags[idx] = cat
                            idx = idx + 1
                            
                    # Once the text is tagged, add it to the result
                    result.append({
                        _id : enumerate(tags)
                    })
                    
                    # Update
                    left -= 1
                       
                # View and save results
                if op == 0: continue
                ViewSave(result)
                
            except Exception as e:
                content = json.dumps(result,indent=4,ensure_ascii=False)
                error = "Corpus:%s, Review:%i, Description:%s Partial:%s" % (source,id,str(e),content)
                log(error)
                raw_input("Reason: %s\nEnter to continue..." % str(e))
                
if __name__=='__main__':
    start()
    