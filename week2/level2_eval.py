import os
import argparse
import csv
from pathlib import Path
import fasttext
import pandas as pd
import warnings
# get rid of future warnings of pandas
warnings.simplefilter(action='ignore', category=FutureWarning)


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

args = parser.parse_args()
model_uri = args.model

if model_uri is None:
    error('model cannot be None')
    exit(42)

output_file = Path(model_uri).parent.as_posix() + os.path.sep + "eval.txt"

test_set = ["iphone", "headphones", "laptop", "freezer", "nintendo", "whirlpool", "kodak", "ps2", "razr", "stratocaster", "holiday", "plasma", "leather"]

model = fasttext.load_model(model_uri)

df = pd.DataFrame(columns=['query', 'synonym', 'estimate'])
for q in test_set:
    nn = model.get_nearest_neighbors(q, k=int(args.max))
    for entry in nn:
        if not is_plural_or_substr(q, entry[1]) and entry[0] > float(args.threshold):
            print("%s: %s" % (q, str(entry)))
            df = df.append({'query': q, 'synonym': entry[1], 'estimate': entry[0]}, ignore_index=True)

df.to_csv(output_file, sep='\t', index=False, header=False, quoting=csv.QUOTE_NONE)