# TODO: Figure out how to configure haystack to register indices in
#       ./indices/<IndexName> instead of this default file...

from haystack import indexes
from django.utils import timezone
from django.db.models import Q

from api_v2.models.Name import Name as NameModel
from api_v2.models.Topic import Topic as TopicModel


class NameIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="text")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((obj.text))

    def get_model(self):
        return NameModel

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            create_timestamp__lte=timezone.now()
        )


class TopicIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # source_id = indexes.CharField(model_attr="text")

    autocomplete = indexes.EdgeNgramField()

    name = indexes.CharField()
    location = indexes.CharField()
    historical = indexes.BooleanField()

    @staticmethod
    def prepare_name(obj):
        print(obj.id)
        print(obj.type)

        # exclude_list = TopicModel.objects.exclude(id=obj.id)

        # for credential in obj.credentials.filter(end_date=None, ):

        for credential in obj.credentials.filter(end_date=None):
            print(credential.topics.all())
            for name in credential.names.all():
                print(name.text)

        print("---")
        return " "

    # @staticmethod
    # def prepare_location(obj):
    #     return " ".join((obj.source_id))

    # @staticmethod
    # def prepare_historical(obj):
    #     return " ".join((obj.source_id))

    def get_model(self):
        return TopicModel

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            create_timestamp__lte=timezone.now()
        )
