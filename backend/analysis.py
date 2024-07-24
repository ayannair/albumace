#!/usr/bin/env python
# coding: utf-8

# ## Separating Transcription into Background Context and Actual Review

# In[83]:


import re
import nltk
nltk.download('punkt')


# In[84]:


# Load the transcript from a file
file_name = '/Users/ayannair/Documents/projects/fantanosize/backend/transcript.txt'
with open(file_name, 'r') as file:
    text = file.read()

# Split the text into sentences
sentences = nltk.sent_tokenize(text)

# Define keywords for each topic
keywords = {
    'lyrics': ['lyrics', 'words', 'writing', 'verses', 'chorus', 'hook', 'poetry', 'lines', 'storytelling', 'themes', 'message', 'narrative', 'bars', 'line'],
    'production': ['beat', 'melody', 'harmony', 'rhythm', 'production', 'sound', 'instrumentation', 'arrangement', 'synths', 'bass', 'drums', 'guitar', 'keys', 'mix', 'mastering', 'sonically'],
    'features': ['feature', 'collaboration', 'guest', 'featuring', 'appearance', 'cameo', 'contribution'],
    'vocals': ['vocals', 'singing', 'rap', 'voice', 'delivery', 'performance', 'flow'],
    'concept': ['concept', 'theme', 'cohesion', 'consistency', 'flow', 'structure', 'production quality', 'about'],
}

topic_sentences = {topic: '' for topic in keywords}

for sentence in sentences:
    for topic, words in keywords.items():
        if any(word in sentence.lower() for word in words):
            topic_sentences[topic] += sentence + ' '


# Print sentences about each topic
for topic, sent in topic_sentences.items():
    print(f"\n{topic.capitalize()} Sentences:")
    print(sent)

# Find the last sentence with the word "feeling"
target_index = None
for i, sentence in enumerate(sentences):
    if 'feeling a' in sentence.lower() or 'feeling' in sentence.lower() or 'strong' in sentence.lower() or 'light' in sentence.lower() or 'decent' in sentence.lower() or 'not good' in sentence.lower():
        target_index = i

# Check if we found a sentence with "feeling"
if target_index is not None:
    # Ensure we have enough sentences before
    start_index = max(target_index - 5, 0)
    end_index = target_index+1

    # Extract the segment
    review_seg = ' '.join(sentences[start_index:end_index])
    print("Review Segment:")
    print(review_seg)
else:
    print("No sentence containing 'feeling a' was found.")


# ## BERT Model Sentiment Analysis

# In[85]:


from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import json
import torch


# In[86]:


MODEL = "cardiffnlp/twitter-roberta-base-sentiment"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


# In[87]:


# Define weights for each sentiment type
weights = {
    'neg': 0.1,
    'neu': 0.2,
    'pos': 0.7
}


# ## Lyrics Analysis

# In[88]:


# Tokenize the input text
encoded_text = tokenizer(topic_sentences["lyrics"], return_tensors='pt', truncation=True, padding=True, max_length=512)

# Ensure no issues with input dimensions
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']

# Perform sentiment analysis
with torch.no_grad():
    output = model(input_ids=input_ids, attention_mask=attention_mask)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    
# Extract numerical values
lyrics_scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}

print(lyrics_scores_dict)

# Compute the combined sentiment score
combined_score = (lyrics_scores_dict['roberta_neg']*weights['neg'] + lyrics_scores_dict['roberta_neu']*weights['neu'] + lyrics_scores_dict['roberta_pos']*weights['pos'])

# Normalize the score
lyrics_normalized_score = combined_score/0.7*100

print(lyrics_normalized_score)


# ## Production Analysis

# In[89]:


# Tokenize the input text
encoded_text = tokenizer(topic_sentences["production"], return_tensors='pt', truncation=True, padding=True, max_length=512)

# Ensure no issues with input dimensions
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']

# Perform sentiment analysis
with torch.no_grad():
    output = model(input_ids=input_ids, attention_mask=attention_mask)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    
# Extract numerical values
prod_scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}

print(prod_scores_dict)

# Compute the combined sentiment score
combined_score = (prod_scores_dict['roberta_neg']*weights['neg'] + prod_scores_dict['roberta_neu']*weights['neu'] + prod_scores_dict['roberta_pos']*weights['pos'])

# Normalize the score
prod_normalized_score = combined_score/0.7*100

print(prod_normalized_score)


# ## Features Analysis

# In[90]:


# Tokenize the input text
encoded_text = tokenizer(topic_sentences["features"], return_tensors='pt', truncation=True, padding=True, max_length=512)

# Ensure no issues with input dimensions
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']

# Perform sentiment analysis
with torch.no_grad():
    output = model(input_ids=input_ids, attention_mask=attention_mask)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    
# Extract numerical values
feat_scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}

print(feat_scores_dict)

# Compute the combined sentiment score
combined_score = (feat_scores_dict['roberta_neg']*weights['neg'] + feat_scores_dict['roberta_neu']*weights['neu'] + feat_scores_dict['roberta_pos']*weights['pos'])

# Normalize the score
feat_normalized_score = combined_score/0.7*100

print(feat_normalized_score)


# ## Vocals Analysis

# In[91]:


# Tokenize the input text
encoded_text = tokenizer(topic_sentences["vocals"], return_tensors='pt', truncation=True, padding=True, max_length=512)

# Ensure no issues with input dimensions
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']

# Perform sentiment analysis
with torch.no_grad():
    output = model(input_ids=input_ids, attention_mask=attention_mask)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    
# Extract numerical values
vocals_scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}

print(vocals_scores_dict)

# Compute the combined sentiment score
combined_score = (vocals_scores_dict['roberta_neg']*weights['neg'] + vocals_scores_dict['roberta_neu']*weights['neu'] + vocals_scores_dict['roberta_pos']*weights['pos'])

# Normalize the score
vocals_normalized_score = combined_score/0.7*100

print(vocals_normalized_score)


# ## Concept Analysis

# In[92]:


# Tokenize the input text
encoded_text = tokenizer(topic_sentences["concept"], return_tensors='pt', truncation=True, padding=True, max_length=512)

# Ensure no issues with input dimensions
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']

# Perform sentiment analysis
with torch.no_grad():
    output = model(input_ids=input_ids, attention_mask=attention_mask)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    
# Extract numerical values
concept_scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}

print(concept_scores_dict)

# Compute the combined sentiment score
combined_score = (concept_scores_dict['roberta_neg']*weights['neg'] + concept_scores_dict['roberta_neu']*weights['neu'] + concept_scores_dict['roberta_pos']*weights['pos'])

# Normalize the score
concept_normalized_score = combined_score/0.7*100

print(concept_normalized_score)


# ## Overall Analysis

# In[93]:


# Tokenize the input text
encoded_text = tokenizer(review_seg, return_tensors='pt', truncation=True, padding=True, max_length=512)

# Ensure no issues with input dimensions
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']

# Perform sentiment analysis
with torch.no_grad():
    output = model(input_ids=input_ids, attention_mask=attention_mask)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    
# Extract numerical values
review_scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}

print(review_scores_dict)

# Compute the combined sentiment score
combined_score = (review_scores_dict['roberta_neg']*weights['neg'] + review_scores_dict['roberta_neu']*weights['neu'] + review_scores_dict['roberta_pos']*weights['pos'])

# Normalize the score
review_normalized_score = combined_score/0.7*100

print(review_normalized_score)


# In[94]:


scores_dict = {
    'lyrics_score': lyrics_normalized_score,
    'production_score': prod_normalized_score,
    'features_score': feat_normalized_score,
    'vocals_score': vocals_normalized_score,
    'concept_score': concept_normalized_score,
    'overall_score' : review_normalized_score
}

json_output = json.dumps(scores_dict, indent=4)

print(json_output)

results_fp = '/Users/ayannair/Documents/projects/fantanosize/backend/results.json'
with open(results_fp, 'w') as json_file:
    json.dump(scores_dict, json_file, indent=4)

