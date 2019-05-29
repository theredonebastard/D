# Implement LDA topic model for further classification
# text_data - prepared aricles by period
class LDAmodel:
            
    def __init__(self, num_topics):
        self.num_topics = num_topics #number of topics
    @staticmethod 
    def _tuple_to_vector(tuple_list, num_topics):
        topic_vector = [0] * (num_topics)
        for t in tuple_list:
            topic_vector[t[0]] = t[1]
        return topic_vector
    
    @staticmethod
    def topic(text_data):
        lda = gensim.models.ldamodel.LdaModel.load("../input/ldamodels/ldamodels/LDAmodel50")
        print("Number of topics", lda.num_topics)
#         print("Keywords of topics", lda.print_topics(lda.num_topics, num_words=5))
        id2word = corpora.Dictionary(text_data)#словарь делается для того чтобы дальше преобразовывать в бов или тфидф
        corpus_bow = [id2word.doc2bow(text) for text in text_data]
        tfidf = models.TfidfModel(corpus_bow)
        corpus_tfidf = tfidf[corpus_bow]
        doc_topic = []
        for nn in range(0, len(text_data)):
            tmp = lda.get_document_topics(corpus_tfidf[nn])
            doc_topic.append(LDAmodel._tuple_to_vector(tmp,lda.num_topics))#veroyatnosti
        return doc_topic
    
    @staticmethod
    def art_keywords(text, nbkeywords):
        
                        
        return keywords(text,words=nbkeywords,scores = True,split=True)#pochitat