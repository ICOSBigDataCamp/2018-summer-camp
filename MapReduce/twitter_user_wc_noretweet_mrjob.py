import json
import mrjob
from mrjob.job import MRJob

class UserWordCountNoReTweet(MRJob):
    INPUT_PROTOCOL = mrjob.protocol.RawValueProtocol #RawValueProtocol takes the entire line as the input value to the mapper. Assumes no key
    OUTPUT_PROTOCOL = mrjob.protocol.RawValueProtocol #In the reducer, ignores the output key and only writes the value to file
    
    def mapper(self, _, line): 
        tweet = json.loads(line)
        if 'retweeted_status' not in tweet:
            screen_name = tweet['user']['screen_name']
            text = tweet['text'] # This is the tweet content (e.g. '@NeilECollins @nyc311 Thank you for reading, Mr. Collins.  Having a TLC driver license is a privilege.')

            ## Basic tokenization: Split the tweet text into words by whitespace
            words = text.split() #['@NeilECollins', '@nyc311', 'Thank', 'you', 'for', 'reading,', 'Mr.', 'Collins.', 'Having', 'a', 'TLC', 'driver', 'license', 'is', 'a', 'privilege.']
            for word in words:
                if word[0] != '@' and word[:4] != "http": # Filter out @mentions (e.g. @nyc311) and links (e.g. https://t.co....)
                    word = word.lower()

                    yield (screen_name, word), 1  #Note that the output key is a tuple of screen name and word.
    
    def reducer(self, key0, counts): #key=(screen_name, word), value=counts
        screen_name, word = key0
        total = 0
        for i in counts: # counts is an iterator. Since the mapper yielded 1 values, it consists of a series of 1's.
            total += i 
        output = screen_name + '\t' + word + '\t' + str(total)
        yield '', output
        
if __name__ == "__main__": 
    UserWordCountNoReTweet.run()
