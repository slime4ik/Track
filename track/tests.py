from django.test import TestCase
from track.models import Track, TrackAnswer, TrackCategory
from account.models import User
from django.urls import reverse
from rest_framework import status
from .pagination import TrackListPagination
# from rest_framework.test import APIRequestFactory # Для пост запросов
from rest_framework.test import APIClient  # Для пост запросов

class TrackListTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='test')
        cat1 = TrackCategory.objects.create(name='Linux')
        cat2 = TrackCategory.objects.create(name='Windows')
        # Создаем 4 трека для проверки пагинации на 3 страницы
        track1 = Track.objects.create(subject='Subject1234',
                             description='description1',
                             creator=user)  # cat=Windows
        track1.category.set([cat2])
        track2 = Track.objects.create(subject='Subject123',
                             description='description12',
                             creator=user)  # cat=Windows
        track2.category.set([cat2])
        track3 = Track.objects.create(subject='Subject12',
                             description='description123',
                             creator=user)  # cat=Linux
        track3.category.set([cat1])
        track4 = Track.objects.create(subject='Subject1',
                             description='description1234',
                             creator=user)  # cat=Linux
        track4.category.set([cat1])
        
    def test_get_track_list_with_pagination(self):
        response = self.client.get(reverse('tracks'))

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Проверка количества объектов
        assert len(data['results']) == TrackListPagination.page_size # берем page_size из кастомной пагинации
        # Проверка содержимого
        subjects = [track['subject'] for track in data['results']]
        assert 'Subject1' in subjects
        assert 'Subject12' in subjects
        assert 'Subject123' in subjects
    
        # Проверка структуры
        for track in data['results']:
            assert 'id' in track
            assert 'subject' in track
            assert 'description' in track
            assert 'creator' in track
        # Проверка пагинации на 2ой странице должен отобразиться 4ый track
        response = self.client.get(reverse('tracks') + '?page=2')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        subjects = [track['subject'] for track in data['results']]
        # Проверяем нит ли треков с 1ой страницы
        assert 'Subject1234' in subjects
        assert 'Subject1' not in subjects
        assert 'Subject12' not in subjects
        assert 'Subject123' not in subjects

    def test_filtering_and_search(self):
        # Проверка фильтрации по категориям
        response = self.client.get(reverse('tracks') + '?category=Linux')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        subjects = [track['subject'] for track in data['results']]
        # Получили треки только с cat=Linux
        assert 'Subject1' in subjects
        assert 'Subject12' in subjects
        assert 'Subject123' not in subjects
        assert 'Subject1234' not in subjects
        # Проверка поиска по id
        track = Track.objects.get(subject='Subject1')
        response = self.client.get(reverse('tracks') + f'?search={track.id}')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        subjects = [track['subject'] for track in data['results']]
        # Проверяем нит ли треков с 1ой страницы order_by('-created_at')
        assert 'Subject1' in subjects
        assert 'Subject12' not in subjects
        assert 'Subject123' not in subjects
        assert 'Subject1234' not in subjects

class TrackListPostCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = APIClient()
        self.url = reverse('tracks')
        self.category = TrackCategory.objects.create(name='Linux')
    # Не авторизированый пользователь пытается сделать трек 
    def test_track_create_unauthenticated(self):
        response = self.client.post(self.url, {
            'subject': 'Test',
            'description': 'Test description',
            'category': [self.category.id]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    # Авторизированый пользователь пытается сделать трек 
    def test_track_create_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            'subject': 'Test',
            'description': 'Test description',
            'category_ids': [self.category.id]
        }, format='json')
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Track.objects.count(), 1)
        self.assertEqual(Track.objects.first().subject, 'Test')
