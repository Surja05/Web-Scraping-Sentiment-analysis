# importing the libraries required

from collections import Counter
from nltk.corpus.reader import sentiwordnet
import requests
import bs4
import string
import re
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# creating a method to parse and extract data from the url provided;
# Data cleaning, tokenization and emotion checking is added too.

def extract(url):

    # url = str(input("Please enter the url from where you want to extract the Information:\n"))

    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
                
    r= requests.get(url, headers=headers)
    htmlcontent  = r.content

    # Parsing the html content using Beautiful Soup
     
    soup = bs4.BeautifulSoup(htmlcontent,"html.parser")

    article_title = soup.find("span",class_ = "td-bred-no-url-last").text
    article_body = soup.find("div", class_ = "td-post-content",).text

    directory = (r"")
    
    # get fileName from user
    filepath = directory + input("Enter filename: ")
    
    # Creates a new file
    with open(filepath, 'w', errors = "ignore") as f:
        f.write(article_title)
        f.write(article_body) 
    
    
    with open(filepath,"r") as f:
        text = f.read()
        
    lower_case = text.lower()
    
    cleaned_text = lower_case.translate(str.maketrans("","",string.punctuation))

    tokenized_text = word_tokenize(cleaned_text,"english")

    final_text_list = []

    for word in tokenized_text:
        if word not in stopwords.words("english"):
            final_text_list.append(word)

    # print(final_text_list)

    emotion_list = []
    with open("emotions.txt","r") as f:
        for line in f:
            cleaned_emotions = line.replace("\n", "").replace("'","").replace(",","").strip()
            word,emotion = cleaned_emotions.split(":")
            
            if word in final_text_list:
                emotion_list.append(emotion)
            
    # print(emotion_list)
    
    # method to get the values for sensitive analysis. Using nested methods to get results

    # def sentiment_analysis(text):
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    pos = score["pos"]
    print(f"Positive Score {pos}")
    neg = score["neg"]
    print(f"Negetive Score {neg}")
    if pos>neg:
        print("Positive Sentiment is observed")
    elif neg>pos:
        print("Negetive Sentiment is observed")
    else:
        print("Neutral Sentiment is observed")
            
    #Polarity Score

    pol = ((pos-neg)/(pos+neg)+ 0.000001)
    print(f"The Polarity score is {pol}")

    # ubjective Score   
    
    subj = ((pos+neg)/(len(text))+ 0.000001)
    print(f"The Subjectivity score is {subj}")

    # Word count on the clean text(removed punctuations and stopwords)

    # def word_count(text):
    # from nltk.tokenize import word_tokenize

    no_of_words = len(word_tokenize(cleaned_text))
    print(f"The Word Count : {no_of_words}")

    # Avg Word length = total no of characters / total no of words
    
    # def avg_word_len(text):
    # from nltk.tokenize import word_tokenize

    no_of_chars = 0
    for word in word_tokenize(cleaned_text):
        no_of_chars  = no_of_chars+ len(word)

    avg_word_len = no_of_chars / no_of_words
    print(f"Avg_word_length : {avg_word_len}")

    # avg no of words per sentence = no_of_words / no_of_sentences

    # def avg_no_of_words_per_sent(text):
    # from nltk.tokenize import word_tokenize,sent_tokenize

    no_of_sents = len(sent_tokenize(cleaned_text))
    avg_no_of_words_per_sent = (no_of_words / no_of_sents)
    print(f"The Avg no of words per Sentence : {avg_no_of_words_per_sent}")

    # Method to print syllables
    
    # def syllable_count(word):
    # word = word.lower()
    
    words=word_tokenize(cleaned_text)
    vowels = "a","e","i","o","u","y"
    no_of_syllables = 0
    for word in words:
        if word[0] in vowels:
            no_of_syllables = no_of_syllables+1
    
    for index in range (1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            no_of_syllables = no_of_syllables+1
    
    if word.endswith("e"):
        no_of_syllables = no_of_syllables - 1

    if no_of_syllables == 0:
        no_of_syllables = no_of_syllables+1

    print(f"The No of syllables present:{no_of_syllables}")  

    # Method to count the complex numbers

    # def complex_word_count(text):
    # from nltk.tokenize import word_tokenize
    words=word_tokenize(cleaned_text)
    complex_word = 0
    for word in words:
        if (no_of_syllables>2):
            complex_word = complex_word+1
    
    print(f"The complex word count : {complex_word}")
    
    # Method for the percentage of complex numbers

    # def percent_complex(text):
    # from nltk.tokenize import word_tokenize
    
    complex_percent = (complex_word/ no_of_words)*100
    print(f"The Percentage of complex words : {complex_percent}")
    
    # Fog Index

    # def fog_index(text):
    # avg_sent_length = avg_no_of_words_per_sent()
    
    fog_read = 0.4*(avg_no_of_words_per_sent/ complex_percent)
    print(f"The Fog Index : {fog_read}")

    
    # Method to find personal Pronoun Count
    # def personal_pronoun(text):
    
    count = 0
    if "I" in text:
        pronoun = re.split("I", text)
        count = count+1
        if "us" in text:
            pronoun = re.split("us", text)
            count = count+1
            if "we" in text:
                pronoun = re.split("we", text)
                count = count+1
                if "my" in text:
                    pronoun = re.split("my", text)
                    count = count+1
                    if "ours" in text:
                        pronoun = re.split("ours", text)
                        count = count+1
                        
        
    print(f"Number of pronouns present: {count}")  

    


with open("abc.txt","r") as f:
        for line in f:
            e = extract(line)
            print(e)
            


        
            


