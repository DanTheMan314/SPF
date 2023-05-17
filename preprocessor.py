import re
from django.utils.html import strip_tags

def remover(text):
    patterns = {
        r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+\b)': '',   #pattern for email id
        r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?': '', #pattern for url
        r'(@|#)\S+': '', #pattern for user-mention and hashtag
        '&[rl]dquo;': '',
        '&[rl]squo;': '',
        ' ': ''    
    }
    
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  #emoticons
                               u"\U0001F300-\U0001F5FF"  #symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  #transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  #flags (iOS)
                               u"\U00002500-\U00002BEF"  #chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  #dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)

    final_text = strip_tags(text)   #remove html tags
    final_text = emoji_pattern.sub(r'', final_text) #remove emoji
    for pattern, repl in patterns.items():
        final_text = re.sub(pattern, repl, final_text) #remove the rest
    return final_text

def preprocess_tool(comments):
    for i in range(0, len(comments)):
        comments[i][0] = remover(comments[i][0])
        if len(comments[i][1]) > 0:
            for j in range(0, len(comments[i][1])):
                comments[i][1][j] = remover(comments[i][1][j])
    return comments