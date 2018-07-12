## Mimir

### Project Structure
- Building Intro
    - Use <a href="https://github.com/pypa/pipenv">`pipenv`</a> as python packaging tool.
    - Use <a href="https://www.djangoproject.com/">`django v2.0+`</a> as website framework.
    - Use <a href="https://github.com/nvbn/django-bower">`django-bower`</a> to `bower` the js packages. 
- About the dashboard design
    - Use `https://github.com/almasaeed2010/AdminLTE` as dashboard template.
- Inside the django structure
    - App `api` as function serving place.
    - App `front_end` as website_frontend pages routing place.
    
- Before Building
    - 1. Install `Node` + `npm` first, and then install **bower** with `npm install bower -g`.
    - 2. Install **pipenv** first with `pip install pipenv`.
- Building steps
    - 1. `cd mimir` change directory into mimir porject.
    - 2. `pipenv install` to initialize the virtualenv and install the needed python packages.
    - 3. `pipenv shell` to activate the virtualenv.
    - 4. `python manage.py bower install` to install needed js, and select the `jquery#3.2.1 which resolved to 3.2.1` choice to finish the install step.
    - 5. `python manage.py runserver localhost:8000` to run the server at `port 8000`.---

---

### Some Memo
- About naming parameters
    - word 單字
    - sentence 句子
    - text 文本
- About naming style
    - 以return之類別作為變數結尾：
        - 如combined_text_string,  words_list, cowords_dict     
    - 以動詞作為function命名開頭、並將相似類別作為結尾分別：
        - 如cut_sentence_ch, cut_sentecne_en

### Chinese Text Preprocessing

Preprocess Chinese text example with `api.preprocess.views` functions.
<pre>
text = """
比特幣在 2 月初慘摔至六千美元附近後止穩反彈，如今又飆回一萬美元整數大關，短短兩個星期漲幅就高達 70％。資料顯示，有人在低點附近逢低狂買了 4 億美元，讓不少站在多方的投資人堅信，6,000 美元可能就是比特幣的底部區。
CoinMarketCap 報價顯示，比特幣這波最低曾在 2 月 6 日摔至 6,048.26 美元，之後開始一路往上漲，至 2 月 16 日盤中最高一度上探 10,324.10 美元，期間漲幅高達 70.7%。
MarketWatch 報導，比特幣錢包地址（bitcoin address）為「3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64」的未具名投資者，在 2 月 9 日至 2 月 12 日期間，擁有的比特幣數量從原本的 55,000 枚一路增加至超過 96,000 枚，購買金額直逼 4 億美元。
Tetras Capital 創辦合夥人 Alex Sunnarborg 說，雖不確定這名買家是誰，但就他所知，許多人也都在比特幣拉回時逢低進場，還在報價反彈、美國與亞洲的法令日益明朗化之際時加碼下注。
比特幣等虛擬貨幣群魔亂舞，引發全球關注。不過，美國投資大師華倫巴菲特（Warren Buffett）警告，這些虛擬貨幣都不會有好下場，若有虛幣賣權這種商品，他會毫不猶豫地買進。
"""

# 去除多餘空白
text = remove_space_marks_ch(text)

# 分句
custom_sent_marks = "，;；。！？!?"
sentences = cut_sentence_ch(text, custom_sent_marks)

# 清除標點符號
custom_mark = ['[’!"#$%&\'()*+-/:;<=>?@[\\]^_`。{|}~「」＜＞〈〉《》【】（）？：、！+“”]', '\n', '\xa0', ' ', '\u3000', '\u200b', '\t']
markoff_sentences = [remove_punctuation(sent, custom_mark) for sent in sentences]

# 載入個人字典, 個人停止詞
# set_jieba_dictionary()
# load_jieba_userdict()
# set_jieba_stop_words()

# 斷詞
tokens_list_in_sents = [tokenize_ch(sent) for sent in markoff_sentences]
merge_tokens_list =[]
for tokens_list in tokens_list_in_sents:
    merge_tokens_list.extend(tokens_list)
    
# 詞數量
tokens_count = get_tokens_count(merge_tokens_list)
    
# 詞頻
sorted_tokens_freqdist = get_tokens_freqlist(merge_tokens_list, 2, 2)

</pre>

Preprocess English text example with `api.preprocess.views` functions.
<pre>
text = """
What Comes Next for the Bitcoin Price?
Bitcoin and other similar currencies have seen a major price drop in early 2018. Most markets lost nearly 50% of their value in a matter of weeks. Many people assume this is the end for cryptocurrency as we know it. True aficionados are not too bothered by this yearly cycle. Tone Vays, a New York-based analyst and consultant, remains positive about the future Bitcoin price.
In Vays’ opinion, Bitcoin will recover sooner rather than later. He is not too sure how high the value will go when the markets start to stabilize again. Reaching six-digit figures will prove to be virtually impossible at this stage. A more “modest” Bitcoin price of $25,000 by year’s end is in Vays’ books right now. Ronnie Moas, another famous Bitcoin enthusiasts, thinks along the same lines. His prediction puts the Bitcoin price at $28,000 at some point throughout 2018.
That optimism is not shared by everyone in the industry. James Rickards, strategic director at financial analytics firm Meraglim, is extremely bearish. Having a more balanced view from both sides of the spectrum is always needed. According to Rickards, the current valuation of Bitcoin is still far too high. Given the speculative nature of this cryptocurrency, it is evident the markets can swing in either direction. Rickards added :

“I don’t know how anybody could set and justify a price target that high for this year. I think bitcoin is going to go to $200. The only residual use is for criminals, and it will keep grinding down.”

Bitcoin Futures and South Korea
Speaking of interest in Bitcoin, there are some positive signs as well. We see a growing interest in Bitcoin futures offered by CME. Their volume for February 2018 currently sits at 1,101. It is the second-highest number for this week, indicating people have high expectations for the Bitcoin price moving forward. CBOE, on the other hand, has seen a volume of 4,225. These numbers are still low, but a definite improvement compared to a few weeks ago. The five-day average volume for both companies is rising. That won’t automatically translate to a higher Bitcoin price, though.

Last but not least, things are moving along in South Korea again. After a few rough weeks, the premium price for Bitcoin is increasing. This is often the result of lower market liquidity and people being forced to pay more per BTC. Bithumb and Upbit trade Bitcoin at nearly $11,400. The Western world trades $900 to $1,000 lower as of right now. This discrepancy has been present before as well. When it happened previously, the global value per Bitcoin soared to $19,000. History may very well repeat itself in this regard.
"""

# 去除多餘空白
text = remove_space_marks_en(text)

# 分句
sentences = cut_sentence_en(text)

# 清除標點符號
custom_mark = ['[!"#%&\()*+-/:;<=>?@[\\]^_`。{|}~「」＜＞〈〉《》【】（）？：、！+“”]', '\n', '\xa0', '\u3000', '\u200b', '\t']
markoff_sentences = [remove_punctuation(sent, custom_mark) for sent in sentences]

# 載入個人字典, 個人停止詞
# set_jieba_dictionary()
# load_jieba_userdict()
# set_jieba_stop_words()

# 斷詞
tokens_list_in_sents = [tokenize_en(sent) for sent in markoff_sentences]
merge_tokens_list =[]
for tokens_list in tokens_list_in_sents:
    merge_tokens_list.extend(tokens_list)
    
# 詞數量
tokens_count = get_tokens_count(merge_tokens_list)
    
# 詞頻
sorted_tokens_freqdist = get_tokens_freqlist(merge_tokens_list, 2, 2)
</pre>

TFIDF Example, with functions in `api.views` and `preprocess.views`.
<pre>
text1 = "火車快飛"
text2 = "火車好美麗"
text3 = "火車是交通工具"
text_list = [text1, text2, text3]
key_list = ["A", "B", "C"]

# Create space_seg_textslist
space_seg_textslist = [remove_punctuation(join_tokens_list_to_string(tokenize_ch(text)), punctuation_list=['[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`，。{|}~「」＜＞〈〉《》【】（）？：、！+*＊“”]', '\n', '\xa0', '  ', '\u3000', '\u200b', '\t']) for text in text_list]

# Create tfidf_ready_dict
tfidf_ready_dict = transfer_textslist_to_tfidfreadydict(space_seg_textslist, key_list)

# TFIDF
get_tfidf(tfidf_ready_dict, 
          content_language="ch", 
          stop_words_txt_path="./jieba_data/stop_words.txt",
          min_tfidf=0.6,
          max_tfidf=1)
</pre>
