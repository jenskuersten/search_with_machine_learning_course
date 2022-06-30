import os
import argparse
import csv
from pathlib import Path
import fasttext
from nltk.stem import SnowballStemmer

def is_plural_or_substr(input, test):
    if input + 's' == test or input[:-1] == test or input[:-2] == test:
        return True
    else:
        return False

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--model", default=None,  help="The model file to be evaluated")
general.add_argument("--threshold", default=0.0,  help="The similarity cut-off threshold")
general.add_argument("--max", default=10,  help="The maximum no. of synonyms per term")
general.add_argument("--input", default=None,  help="The input file with one term per line")
general.add_argument("--output", default="synonyms.csv",  help="The output file with synonyms")

args = parser.parse_args()
model_uri = args.model

if model_uri is None:
    error('model cannot be None')
    exit(42)

output_file = Path(model_uri).parent.as_posix() + os.path.sep + args.output

print("Reading input data")
test_set = set()
if args.input is not None:
    try:
        with open(args.input) as f:
            for line in f.readlines():
                test_set.add(line.strip())
    except IOError:
        print("File not accessible")
else:
    test_set = ["iphone", "headphones", "laptop", "freezer", "nintendo", "whirlpool", "kodak", "ps2", "razr", "stratocaster", "holiday", "plasma", "leather"]

print("Loading model")
model = fasttext.load_model(model_uri)

stemmer = SnowballStemmer("english")

print("Creating output")
with open(output_file, 'w') as output:
    for q in test_set:
        nn = model.get_nearest_neighbors(stemmer.stem(q), k=int(args.max))
        synonyms = str("")
        for entry in nn:
            if not is_plural_or_substr(q, entry[1]) and entry[0] > float(args.threshold):
                print("%s, %s: %.4f" % (q, entry[1], entry[0]))
                if len(synonyms) == 0:
                    synonyms = entry[1]
                else:
                    synonyms +=  ", " + entry[1]
        if (len(synonyms) > 0):
            output.write("%s, %s\n" % (q, synonyms))