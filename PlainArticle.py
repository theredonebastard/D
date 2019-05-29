class PlainArticle:
    title = ''
    text = ''
    summary = ''
    keywords = []
    publish_date = ''
    
    def __init__(self, title, text, summary, keywords, publish_date):
        self.title = title
        self.text = text
        self.summary = summary
        self.keywords = keywords
        self.publish_date = publish_date
        
    def _toList(self):
        return [
            self.title,
            self.text,
            self.summary,
            self.keywords,
            self.publish_date
        ]