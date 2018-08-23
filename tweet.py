import tweepy
from textblob import TextBlob
import nltk 
import string
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re


consumer_key="*****"
consumer_secret="*****"

access_token="*****"
access_token_secret="*****"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

dallas='32.802955,-96.769923,2km'
ny='40.712784,-74.005941,1km'
sf='37.77493,-122.419416,1km'
la='34.052234,-118.243685,1km'
chicago='41.878114,-87.629798,1km'
dc='38.907192,-77.036871,1km'
atlanta='33.748995,-84.387982,3km'

loc=''

def tweetana(keyword):
    count=0
    pol=0
    sub=0
    p=string.punctuation+"'"+'"'
    n=string.digits
    txtp=string.maketrans(p,len(p)*" ")    
    txtd=string.maketrans(n,len(n)*" ")
    stopwords = nltk.corpus.stopwords.words('english')+['https','RT','co']
    printable = set(string.printable)
    ss = SnowballStemmer("english") 
    newword=[]    
    fulllis=[]
    fl=''
    f=open("election/"+keyword+"16.txt",'w')
    for status in tweepy.Cursor(api.search,
                                q=keyword,
                                count=100,
                                result_type='recent',
                                include_entities=True,
                                monitor_rate_limit=True, 
                                wait_on_rate_limit=True,
                                lang="en",
                                since='2016-11-09').items():

   
        #print"\n"
        #print status.user.screen_name,
        #print "--- ",
        #print status.user.location
        #print "--- ",
        #print status.text,
        #print ""
       
        
        if count==500:
            break
    
        words2=[]
        rw=[]
        tw=''
        tweet=TextBlob(status.text)
        #tk=TweetTokenizer(strip_handles=True, reduce_len=True)
        readword=word_tokenize(status.text)
        for w in readword:
            rw.append(filter(lambda x: x in printable, str(w.encode('utf-8'))))
            
        
        newtxt=str(rw).translate(txtp)
        newtxt=newtxt.translate(txtd)
        newword=word_tokenize(newtxt)
        #words2=[w for w in newword if w not in stopwords and len(w)>1]
        for w in newword:
            if len(w)==1 or w in stopwords:
                continue
            words2.append('{}'.format(w))
            tw+='{} '.format(w)
        f.write(str(status.user.screen_name)+" : "+tw+"\n")
        for w in words2:
            fulllis.append(ss.stem(filter(lambda x: x in printable, str(w))))
        
      
        
        tr_pol=tweet.sentiment.polarity
        tr_sub=tweet.sentiment.subjectivity
        pol+=tr_pol
        sub+=tr_sub
        count+=1
    print "___________________________"+keyword.upper()+"______________________"
    for w in fulllis:
        fl+='{} '.format(filter(lambda x: x in printable, str(w)))
    print "\nPolarity="+str(pol/count)
    print "\nSubjectivity="+str(sub/count)
    f.close()
    return fl
    

    
    
def main():

    ft=tweetana("Trump")
    wordcloud1 = WordCloud(max_font_size=40).generate(str(ft))
    figt=plt.figure(figsize=(10,10))
    plt.imshow(wordcloud1)
    plt.axis("off")
    #figt.savefig("Trump_"+loc+".png")
    plt.show()
    
    fh=tweetana("Hillary")
    wordcloud2 = WordCloud(max_font_size=40).generate(str(fh))
    figh=plt.figure(figsize=(10,10))
    plt.imshow(wordcloud2)
    plt.axis("off")
    #figh.savefig("Hillary_"+loc+".png")
    plt.show()
   
    fo=tweetana("Obama")    
    wordcloud3 = WordCloud(max_font_size=40).generate(str(fo))
    figo=plt.figure(figsize=(10,10))
    plt.imshow(wordcloud3)
    plt.axis("off")
    #figo.savefig("Obama_"+loc+".png")
    plt.show()


main()

