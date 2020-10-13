import datetime
from haystack import indexes
from chatRoom.models import Chatroom
from datetime import timedelta
from django.utils import timezone

class ChatroomIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Chatroom
