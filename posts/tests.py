from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    ''' Tests for PostView '''
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')
        # run before all tests are run

    def test_can_list_posts(self):
        '''Test a user can list posts'''
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        ''' Test if a verified user can create a post '''
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        ''' Ensures logged out users cant create a post '''
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    '''
    Test retrieve post and edit functionality
    '''
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Post.objects.create(
            owner=adam, title='a title', content='adams content'
        )
        Post.objects.create(
            owner=brian, title='another title', content='brians content'
        )

    def test_retrieve_post_with_valid_id(self):
        '''
        A valid user can retrieve their post
        due to valid ID.
        '''
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post_with_invalid_id(self):
        '''
        A valid user cannot retrieve their post
        due to invalid ID.
        '''
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_owned_post(self):
        '''
        Test a user can update their own post.
        '''
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_unowned_post(self):
        '''
        Test a user cannot update someone else's post.
        '''
        self.client.login(username='brian', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
