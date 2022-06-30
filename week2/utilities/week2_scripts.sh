# level 1 - getting started
python week2/createContentTrainingData.py --output /workspace/datasets/fasttext/labeled_products.txt
shuf /workspace/datasets/fasttext/labeled_products.txt  > /workspace/datasets/fasttext/shuffled_labeled_products.txt
cat /workspace/datasets/fasttext/training_lite.txt  | sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]_]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_training_lite.txt

# level 2 - data/model preparation
shuf /workspace/datasets/fasttext/labeled_products.txt  > /workspace/datasets/fasttext/shuffled_labeled_products.txt
cut -d$'\t' -f2- /workspace/datasets/fasttext/shuffled_labeled_products.txt > /workspace/datasets/fasttext/titles.txt
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/titles.txt -output /workspace/datasets/fasttext/title_model
~/fastText-0.9.2/fasttext nn /workspace/datasets/fasttext/title_model.bin

# level 2 - synonym generation
cat /workspace/datasets/fasttext/titles.txt | sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_titles.txt

# level 3 - integration
cat /workspace/datasets/fasttext/titles_normalized.txt | tr " " "\n" | grep "...." | sort | uniq -c | sort -nr | head -1000 | grep -oE '[^ ]+$' > /workspace/datasets/fasttext/top_words.txt
python ../../search_with_machine_learning_course/week2/generateSynonyms.py --model /workspace/datasets/fasttext/title_normalized_model.bin --threshold 0.66 --max 5 --input top_words.txt