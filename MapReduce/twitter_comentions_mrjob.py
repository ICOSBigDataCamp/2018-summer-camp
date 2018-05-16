import json
import mrjob
from mrjob.job import MRJob
import itertools

class CoMentions(MRJob):
    INPUT_PROTOCOL = mrjob.protocol.RawValueProtocol #RawValueProtocol takes the entire line as the input value to the mapper. Assumes no key
    OUTPUT_PROTOCOL = mrjob.protocol.RawValueProtocol #In the reducer, ignores the output key and only writes the value to file
    
    def mapper(self, _, line): 
        tweet = json.loads(line)
        mentioned = tweet['entities']['user_mentions']
        m_snames=[] #List of the screen names of those who were mentioned
        if len(mentioned) > 1: # If more than one user was mentioned in this tweet
            for each_user in mentioned: 
                m_snames.append( each_user['screen_name'] ) #parse the screen name from the data structure and append it to a list of screen names (m_snames)
            for user_pair in itertools.combinations(m_snames, 2): # Generate pairs of users and iterate through those pairs
                ## itertools.combinations('ABCD', 2) --> AB AC AD BC BD CD
                yield (max(user_pair), min(user_pair)), 1 #Sort the pair so that same pairs end up in the same reducer
            
    def reducer(self, user_pair, counts): #key=(screen_name, word), value=counts
        user_A, user_B = user_pair
        total = 0
        for i in counts: # counts is an iterator. Since the mapper yielded 1 values, it consists of a series of 1's.
            total += i 
        output = user_A + '\t' + user_B + '\t' + str(total)
        yield '', output
        
if __name__ == "__main__": 
    CoMentions.run()
