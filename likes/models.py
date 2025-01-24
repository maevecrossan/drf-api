from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Like(models.Model):
    '''
    Like model, related to 'owner' and 'post'.
    'owner' is a User instance and 'post' is a Post instance.
    'unique_together'/'Constraints' makes
    sure a user can't like the same post twice.
    '''
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE
        )
    created_at = models.DateTimeField(
        auto_now_add=True
        )

    class Meta:
        '''
        'Constraints' makes sure a user can't like the same post twice.
        '''
        ordering = ['-created_at']
        # unique_together = ['owner', 'post']
        # Above is deprecated. Below is recommended replacement.
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'post'],
                name='unique_owner_post_like')
        ]

    def __str__(self):
        return f'{self.owner} {self.post}'
