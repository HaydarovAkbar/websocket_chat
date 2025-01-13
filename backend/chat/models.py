from django.db import models

import uuid
# import timesince
from django.utils.timesince import timesince


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField('auth.User', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Conversation {self.id}'

    def update_at_formatted(self):
        return timesince(self.update_at)

    class Meta:
        ordering = ['-created_at']
        db_table = 'conversation'


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey('auth.User', related_name='messages', on_delete=models.CASCADE)
    sent_to = models.ForeignKey('auth.User', related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Message {self.id}'

    def created_at_formatted(self):
        return timesince(self.created_at)

    class Meta:
        ordering = ['created_at']
        db_table = 'message'
