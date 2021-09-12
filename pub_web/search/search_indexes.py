import datetime
from haystack import indexes
from search.models import Pub


class NoteIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    pub_year = indexes.IntegerField(model_attr='pub_year')

    def get_model(self):
        return Pub

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()