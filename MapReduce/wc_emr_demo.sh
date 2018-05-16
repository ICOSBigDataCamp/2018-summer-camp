#!/bin/bash
# Run the word count example on AWS Elastic Map Reduce

python wordcount_mrjob.py s3://datacamp2018/input/wiki_text_tokens.txt.bz2  \
-r emr \
--no-output \
--output-dir=s3://datacamp2018/wordcount/ \
--conf-path=$HOME'/wc_emr.conf'

