## Again, we import the MRJob class which is the base class of the mrjob library
import json
import mrjob
from mrjob.job import MRJob

class TwitterWordCount(MRJob):
    INPUT_PROTOCOL = mrjob.protocol.RawValueProtocol #RawValueProtocol takes the entire line as the input value to the mapper. Assumes no key
    OUTPUT_PROTOCOL = mrjob.protocol.RawValueProtocol #In the reducer, ignores the output key and only writes the value to file
    
    def mapper(self, _, line): # key is ignored in this example
        tweet = json.loads(line) # Convert raw string into Python object
        text = tweet['text'] # This is the tweet text (e.g. '@NeilECollins @nyc311 Thank you for reading, Mr. Collins.  Having a TLC driver license is a privilege.')
        
        ## Basic tokenization: Split the tweet text into words by whitespace
        words = text.split() #['@NeilECollins', '@nyc311', 'Thank', 'you', 'for', 'reading,', 'Mr.', 'Collins.', 'Having', 'a', 'TLC', 'driver', 'license', 'is', 'a', 'privilege.']
        for word in words:
            if word[0] != '@' and word[:4] != "http": # Filter out @mentions (e.g. @nyc311) and links (e.g. https://t.co....)
                '''
                Basic cleaning of each word: force all characters in a word to lower case. 
                Fancier cleaning techniques are the subject of NLP (e.g. removing punctuation, stemming, etc).
                '''
                word = word.lower() #Force the word to be lower case
                yield word, 1 # Mapper outputs a <key, value> pair: in this case, word as key and 1 as value
    
    def reducer(self, word, counts): #key=word, value=counts
        total = 0 
        for i in counts: # counts is an iterator. Since the mapper yielded 1 values, it consists of a series of 1's.
            total += i 
        output = word + '\t' + str(total)
        yield '', output
        
if __name__ == "__main__": 
    TwitterWordCount.run()
