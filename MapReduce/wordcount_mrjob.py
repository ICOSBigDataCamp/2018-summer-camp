## We import the MRJob class which is the base class of the mrjob library
from mrjob.job import MRJob

class MRWordCounter(MRJob): # We define a class that "interits" the functions contained in the MRJob class.
    def mapper(self, key, line): # The first argument of a function inside a class is always "self". The mapper function takes a key and a value as inputs.
        for word in line.split():
            word = word.lower() # Force all characters to be lower case.
            yield word, 1  # word is the key, 1 is the value which will be fed into the reducer

    def reducer(self, word, occurrences): # occurrences is an iterator that collects all the values of the same key (e.g. [1,1,1,1])
        yield word, sum(occurrences)

if __name__ == '__main__':  # If the Python interpreter executes this as an indepedent script rather than imported in another script, it will run this block.
    MRWordCounter.run() # Run the job that you implemented in MRWordCounter
