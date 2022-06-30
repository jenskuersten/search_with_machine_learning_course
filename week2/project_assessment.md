  ## For classifying product names to categories:

- What precision (P@1) were you able to achieve?
  - P@1 was not even above 0.1!
- What fastText parameters did you use?
  - `-lr 1 -epoch 25 -wordNgrams 2`
- How did you transform the product names?
  - mainly followed the suggestions in the description, by (a) non-alphanumeric chars and punctuations, (b) whitespace stripping, (c) a failed attempt at stemming - can you spot the [bug](https://github.com/gsingers/search_with_machine_learning_course/commit/6147f0dd2590b2d8cdefadafc4da71a76c43547c#diff-35e472638d071ac9aa810dcd8f7cbf7c07ce0b3f426aacd9317da90dc67cf6a5) :D?
- How did you prune infrequent category labels, and how did that affect your precision?
  - again, mainly followed the project description and removed categories with less than 500 products
  - P@1=0.973, see [evaluation file](https://github.com/jenskuersten/search_with_machine_learning_course/blob/main/week2/eval/level1_product_classification_results.txt)
- How did you prune the category tree, and how did that affect your precision?
  - skipped that optional part

## For deriving synonyms from content:

- What were the results for your best model in the tokens used for evaluation?
  - good from my perspective ;) - [see results](https://github.com/jenskuersten/search_with_machine_learning_course/blob/2ba4c6e2ec3ed90b3f612ff93c63f595d5409bf1/week2/eval/level2_synonym_results_normalized_optimized.txt#L7)
- What fastText parameters did you use?
  -  train: `~/fastText-0.9.2/fasttext skipgram -input titles_normalized.txt -output title_normalized_model -epoch 25 -minCount 20`
  -  test: `--threshold 0.75 --k 5`
- How did you transform the product names?
  - stripping html
  - basic tokenizing
  - filtered to alphanumerics plus a few more possbily semantic chars (in the data)
  - stemming (fixed bug from level 1)
  - filter: term length > 1
  - strip whitespaces
  - see [details](https://github.com/jenskuersten/search_with_machine_learning_course/blob/2ba4c6e2ec3ed90b3f612ff93c63f595d5409bf1/week2/createContentTrainingData.py#L18)

## For integrating synonyms with search:

- How did you transform the product names (if different than previously)?
  - see above, I think I changed the punctuation handling, because punctuations like `3.5mm` carry some meaning, but removed `,` to escape escaping problems due to the target format ;)
- What threshold score did you use?
  - reduced the threshold, because on some examples best synonyms like `notebook` for `laptop` had a lower value than 0.75. Also reduced the number of synonyms to return per term, because for some other examples there were a lot of near-duplicates like model numbers or specific size descirptions for `plasma`
  -  test: `--threshold 0.66 --k 5`
- Were you able to find the additional results by matching synonyms?
  - TODO

## For classifying reviews:
- did not get that far due to personal time limitations
