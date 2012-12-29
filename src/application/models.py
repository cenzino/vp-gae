"""
models.py

App Engine datastore models

"""
from google.appengine.ext import db
from utils import slugify


class ExampleModel(db.Model):
    """Example Model"""
    example_name = db.StringProperty(required=True)
    example_description = db.TextProperty(required=True)
    added_by = db.UserProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)

class Category(db.Model):
    name = db.StringProperty(required=True)
    slug = db.StringProperty()

    @property
    def id(self):
        return self.key().id_or_name()
        
    def save(self):
        return self.put()
    
    def put(self, **kwargs):
        self.slug = slugify(self.name)
        self._key_name = self.slug
        return super(Category, self).put(**kwargs)
    
    def delete(self, **kwargs):
        posts = self.post_set
        for p in posts:
            p.category = None
            p.put()
        super(Category, self).delete()
    
    def __str__(self):
        return unicode(self.name)
      
class Post(db.Model):
    """ Modello del Post """
    title = db.StringProperty(required=True)
    text = db.TextProperty()
    html = db.TextProperty()
    
    category = db.ReferenceProperty(Category)
    tags = db.ListProperty(db.Category)
    
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    pubblished_at = db.DateTimeProperty()
    
    draft = db.BooleanProperty(default=True)

    @classmethod
    def convert_string_tags(cls, tags):
        new_tags = []
        for t in tags:
            t = slugify(t)
            if type(t) == db.Category:
                new_tags.append(t)
            else:
                if t != "":
                    new_tags.append(db.Category(unicode(t)))
        return new_tags
    
    def __str__(self):
        return u'({1}) {0} u:{2}'.format(self.title, self.created_at.strftime('%Y/%m/%d %H:%M'), self.updated_at.strftime('%Y/%m/%d %H:%M'))
    
    @property
    def id(self):
        return self.key().id()

    def save(self):
        self.put()
    
    def put(self, **kwargs):        
        """ Salva il post convertendo il testo markdown in html """
        self.html = self.text
        return db.Model.put(self, **kwargs)