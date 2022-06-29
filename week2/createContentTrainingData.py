import argparse
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from nltk.stem import SnowballStemmer
import re
import pandas as pd

def transform_name(product_name):
    input = product_name
    stemmer = SnowballStemmer("english")

    # alphanumeric
    alphanumeric_product_name = re.sub(r'[^A-Za-z0-9 ]+', '', product_name)

    # remove punctuation & brackets
    tokenized_product_name = re.sub('[.\!?,\'/()]', '', alphanumeric_product_name)

    # trim whitespaces
    trimmed_product_name = re.sub('\s+', ' ', tokenized_product_name)

    # loweracase
    normalized_product_name = stemmer.stem(trimmed_product_name.lower())
    
    #print("input: " + product_name + ", normalized: " + normalized_product_name)
    return normalized_product_name

# Directory for product data
directory = r'/workspace/datasets/product_data/products/'

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory,  help="The directory containing product data")
general.add_argument("--output", default="/workspace/datasets/fasttext/output.fasttext", help="the file to output to")
general.add_argument("--label", default="id", help="id is default and needed for downsteam use, but name is helpful for debugging")

# Consuming all of the product data, even excluding music and movies,
# takes a few minutes. We can speed that up by taking a representative
# random sample.
general.add_argument("--sample_rate", default=1.0, type=float, help="The rate at which to sample input (default is 1.0)")

# IMPLEMENT: Setting min_products removes infrequent categories and makes the classifier's task easier.
general.add_argument("--min_products", default=500, type=int, help="The minimum number of products per category (default is 0).")

args = parser.parse_args()
output_file = args.output
path = Path(output_file)
output_dir = path.parent
output_dir_name = output_dir.as_posix() + os.path.sep
output_file_name = re.sub(output_dir_name, '', output_file)

if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)

if args.input:
    directory = args.input
# IMPLEMENT:  Track the number of items in each category and only output if above the min
min_products = args.min_products
sample_rate = args.sample_rate
names_as_labels = False
if args.label == 'name':
    names_as_labels = True

df = pd.DataFrame(columns=['label', 'product_name'])

# print("Writing results to %s" % output_file)
# with open(output_file, 'w') as output:
#     for filename in os.listdir(directory):
#         if filename.endswith(".xml"):
#             print("Processing %s" % filename)
#             f = os.path.join(directory, filename)
#             tree = ET.parse(f)
#             root = tree.getroot()
#             for child in root:
#                 if random.random() > sample_rate:
#                     continue
#                 # Check to make sure category name is valid and not in music or movies
#                 if (child.find('name') is not None and child.find('name').text is not None and
#                     child.find('categoryPath') is not None and len(child.find('categoryPath')) > 0 and
#                     child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text is not None and
#                     child.find('categoryPath')[0][0].text == 'cat00000' and
#                     child.find('categoryPath')[1][0].text != 'abcat0600000'):
#                       # Choose last element in categoryPath as the leaf categoryId or name
#                       if names_as_labels:
#                           cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][1].text.replace(' ', '_')
#                       else:
#                           cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text
#                       # Replace newline chars with spaces so fastText doesn't complain
#                       name = child.find('name').text.replace('\n', ' ')
#                       output.write("__label__%s %s\n" % (cat, transform_name(name)))
#                       df = df.append({'label': '__label__'+cat, 'product_name': transform_name(name)}, ignore_index=True)

# write re-readable pandas data frame
#df.to_csv("%spandas_%s" % (output_dir_name, output_file_name), index=False, header=False)
df = pd.read_csv("%spandas_%s" % (output_dir_name, output_file_name), names=['label', 'product_name'], header=None)

# get frequency of categories and apply filtering
pruned_min = df[df['label'].map(df['label'].value_counts()) >= min_products]

# check if pruning matches expectation
print(pruned_min.head())
print("row count: " + str(len(pruned_min)))

pruned_output_file = "%spruned_%s" % (output_dir_name, output_file_name)
print("Writing results to %s" % pruned_output_file)
pruned_min.to_csv(pruned_output_file, sep=' ', index=False, header=False)