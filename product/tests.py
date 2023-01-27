from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.core.files import File
from collections import OrderedDict

from .views import ProductView
from .models import Products, Category
from account.models import User

class PostTest(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(title='cat1')
        self.user = User.objects.create(email='test@gmail.com', password='1234', name='test', last_name='TEST', is_active=True)
        img = File(open('posts/Screenshot_from_2021-09-16_19-45-28_DB1ohpt.png', 'rb'))
        posts = [Products(author=self.user, body='new_post', title='post1', image=img, category=self.category, slug=1), Products(author=self.user, body='new_post', title='post2', image=img, category=self.category, slug=2),Products(author=self.user, body='new_post', title='post3', image=img, category=self.category, slug=3)]
        Products.objects.bulk_create(posts)
    
    def test_list(self):
        request = self.factory.get(path='post/') 
        view = Products.as_view({'get':'list'})
        responce = view(request)

        assert responce.status_code == 200

    def test_retrive(self):
        slug = Products.objects.all()[0].slug
        request = self.factory.get(path=f'posts/{slug}/')
        view = ProductView.as_view({'get': 'retrieve'})
        responce = view(request, pk=slug)

        assert responce.status_code == 200

    def test_create(self):
        user = User.objects.all()[0]
        data = {'body':'how are you', 'title':'post4', 'category':'cat1'}
        request = self.factory.post('posts/', data, format='json')
        force_authenticate(request, user=self.user)
        view = ProductView.as_view({'post':'create'})
        response = view(request)

        assert response.status_code == 201
        assert response.data['body']== data['body']
        assert Products.objects.filter(author=user, body=data['body']).exists()