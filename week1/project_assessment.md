# Project Assessment

1. Do you understand the steps involved in creating and deploying an LTR model?  Name them and describe what each step does in your own words.
    - Initialization: preparing the software (e.g. LTR plugin) and LTR storage
    - Feature (store) setup: preparing the storage for the feature description and queries
    - Creating a relevance / judgement collection (tuple of: query_id, doc_id, relevance_judgment) to be used for model training and feature engineering
    - Feature logging: collect features from queries or other sources and create a training file (tuple of: query_id, doc_id, feature_val_n ...)
    - Training: train and test a model, typically XGBoost for LTR
    - Model deployment: upload your model so it can be used during query time
    - Search quality assessment: run your test queries and assess the model / configuration quality by using the judgment
1. What is a feature and featureset?
    - Feature is a single attribute or wrapped function that should be used for LTR
    - Feature set is the collection of all feature that can be used for LTR
1. What is the difference between precision and recall?
    - Precision: ratio of relevant items retrieved to retrieved items
    - Recall: ration of relevant items retrieved to all relevant items
1. What are some of the traps associated with using click data in your model?
    - Click data or any type of implicit data is only a proxy for intent. Hence, it may bring different kinds of bias:
      - Position bias
      - Presentation bias
      - Recency bias
      - Popularity bias
      - Query distribution bias
      - ...
1. What are some of the ways we are faking our data and how would you prevent that in your application?
    - We don't know the ranking that produced the impressions, we are using our search engine setup as a proxy (to collect the non-relevant docs)
    - We are using a simple step function with for buckets
    - Clicks alone could be easily created by bot traffic
    - So we would probably want to collect more precise data along with hit sets from the original search engine. We would want to make sure query distribution (e.g. frequency) matches our actual customer behavior...
1. What is target leakage and why is it a bad thing?
    - Exposing the target value for training via the features, which would typically create great assessment results, but the model would in fact be garbage and not suitable for production.
1. When can using prior history cause problems in search and LTR?
    - As soon as the customer behavior changes (e.g. seasonal effects like X-Mas/summer/winter in e-commerce). Also the way this is implemented matters, because it is easy to mess up if your using priors from catalog items. This works for stable catalogs, but could be useless for volatile collections.
1. Submit your project along with your best MRR scores
