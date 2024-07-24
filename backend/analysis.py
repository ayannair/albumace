#!/usr/bin/env python
# coding: utf-8

# ## Separating Transcription into Background Context and Actual Review

# In[412]:


import re
import nltk
nltk.download('punkt')


# In[413]:


# Load the transcript from a file
file_name = '/Users/ayannair/Documents/projects/fantanosize/backend/negative/scaled-and-icy.txt'
with open(file_name, 'r') as file:
    text = file.read()

# Split the text into sentences
sentences = sent_tokenize(text)

# Find the last sentence with the word "feeling"
target_index = None
for i, sentence in enumerate(sentences):
    if 'feeling a' in sentence.lower() or 'transition' in sentence.lower() or 'tran' in sentence.lower():
        target_index = i

# Check if we found a sentence with "feeling"
if target_index is not None:
    # Ensure we have enough sentences before
    start_index = max(target_index - 4, 0)
    end_index = target_index

    # Extract the segment
    review_segment = ' '.join(sentences[start_index:end_index])
    print("Review Segment:")
    print(review_segment)
else:
    print("No sentence containing 'feeling a' was found.")


# ## BERT Model Sentiment Analysis

# In[414]:


from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax


# In[415]:


review_text = "There are other points I guess I could go over like the weird licensing bars on the track Sun Come Down or the lifeless singing and super bland production and non-song that is delivered on the track Town on the Hill but really what's the point at this point? There are so many terrible ideas written and employed on this record, it's either falling short because the base concept is terrible or it's just been carried out in an awful way. I did not love a single song from this album, not one single track. There were moments where I caught a breath of like oh that's, maybe could be decent but it just did not pan out and considering how long this record is and how consistently unbearable a lot of it is, I just don't know what to say."


# In[416]:


MODEL = "cardiffnlp/twitter-roberta-base-sentiment"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


# In[417]:


# Tokenize the input text
encoded_text = tokenizer(review_segment, return_tensors='pt', truncation=True, padding=True, max_length=512)

# Ensure no issues with input dimensions
input_ids = encoded_text['input_ids']
attention_mask = encoded_text['attention_mask']

# Perform sentiment analysis
with torch.no_grad():
    output = model(input_ids=input_ids, attention_mask=attention_mask)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    
# Extract numerical values
scores_dict = {
    'roberta_neg': scores[0],
    'roberta_neu': scores[1],
    'roberta_pos': scores[2]
}

print(scores_dict)


# In[418]:


neg_score = scores_dict['roberta_neg']
neu_score = scores_dict['roberta_neu']
pos_score = scores_dict['roberta_pos']


# Define weights for each sentiment type
weights = {
    'neg': 0.1,  # Weight for negative sentiment
    'neu': 0.2,
    'pos': 0.7   # Weight for positive sentiment
}

# Compute the combined sentiment score
combined_score = (neg_score*weights['neg'] + neu_score*weights['neu'] + pos_score*weights['pos'])

# Normalize the score to the 1-100 range
# Assuming the combined score is already in the 0-1 range (after applying softmax)
normalized_score = combined_score * 100
print(normalized_score/70.0*100)


# In[ ]:




