import json
import itertools
import mrjob
from mrjob.job import MRJob
from mrjob.step import MRStep # A class that allows you to explicitly specify the mapper and the reducer function to use in a step 


class MostCoMentioned(MRJob):
    INPUT_PROTOCOL = mrjob.protocol.RawValueProtocol #RawValueProtocol takes the entire line as the input value to the mapper. Assumes no key
    OUTPUT_PROTOCOL = mrjob.protocol.RawValueProtocol #In the reducer, ignores the output key and only writes the value to file

    def mapper1(self, _, line): 
        tweet = json.loads(line)
        mentioned = tweet['entities']['user_mentions']
        m_snames=[] #List of the screen names of those who were mentioned
        if len(mentioned) > 1: # If more than one user was mentioned in this tweet
            for each_user in mentioned: 
                m_snames.append( each_user['screen_name'] ) #parse the screen name from the data structure and append it to a list of screen names (m_snames)
            for user_pair in itertools.combinations(m_snames, 2): # Generate pairs of users and iterate through those pairs
                ## itertools.combinations('ABCD', 2) --> AB AC AD BC BD CD
                ordered_pair = ( max(user_pair), min(user_pair) )
                yield ordered_pair, 1 #Sort the pair so that same pairs end up in the same reducer
            
    def reducer1(self, user_pair, counts): #key=(screen_name, word), value=counts
        user_A, user_B = user_pair
        total = sum(counts)
        yield user_A, (user_B, total) #yield one record for user_A: In the next reduce step, all comentioned users of user_A will be grouped
        yield user_B, (user_A, total) #yield one record for user_B: In the next reduce step, all comentioned users of user_B will be grouped
    
    def reducer2(self, focal_user, values1):
        max_value=0 #initialize maximum comention value at 0
        for each in values1: # Iterate through each (user, frequency) pair 
            comentioned_user, frequency = each
            if frequency > max_value:
                max_value = frequency #update max_value to the new maximum number of comentions
                max_mentioned = comentioned_user # the new comentioned user with the maximum number of comentions up to this point
        
        ## At the end of the for-loop, we end up with the most frequently co-mentioned user of the focal_user
        
        result_string = focal_user + '\t' + max_mentioned + '\t' + str(max_value)
        yield '', result_string

        
    def steps(self): # Specify the individual mapper and reducer functions to be used 
        first_step = MRStep(mapper=self.mapper1, reducer=self.reducer1) # The first step should execute the above-defined self.mapper and self.reducer1
        second_step = MRStep( reducer=self.reducer2 ) # The output from self.reducer1 is fed straight into self.reducer2 without having to go through a second mapper.
        
        all_steps = [ first_step, second_step ] # Create a list that contains the steps in order
        return all_steps
        
        
if __name__ == "__main__": 
    MostCoMentioned.run() 
