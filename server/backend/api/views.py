from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from dealership_app.models import Dealer, Review, CarMake, CarModel
from dealership_app.serializers import DealerSerializer, ReviewSerializer
from django.http import JsonResponse
import json


@api_view(['GET'])
def get_dealers(request):
    dealers = Dealer.objects.all()
    serializer = DealerSerializer(dealers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_dealer_by_id(request, id):
    try:
        dealer = Dealer.objects.get(id=id)
        serializer = DealerSerializer(dealer)
        return Response(serializer.data)
    except Dealer.DoesNotExist:
        return Response({'error': 'Dealer not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state=state.upper())
    serializer = DealerSerializer(dealers, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def get_dealer_reviews(request, id):
    if request.method == 'GET':
        reviews = Review.objects.filter(dealer_id=id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            dealer = Dealer.objects.get(id=id)
            username = request.data.get('user') or request.data.get('username')
            user = User.objects.filter(username=username).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            review_text = request.data.get('review_text', '')
            rating = request.data.get('rating', 5)
            # simple sentiment
            sentiment = analyze_text(review_text)
            review = Review.objects.create(
                dealer=dealer,
                user=user,
                review_text=review_text,
                rating=rating,
                sentiment=sentiment
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Dealer.DoesNotExist:
            return Response({'error': 'Dealer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def analyze_text(text):
    text_lower = text.lower()
    positive_words = ['great', 'fantastic', 'excellent', 'amazing', 'good', 'love', 'awesome', 'wonderful', 'best']
    negative_words = ['bad', 'terrible', 'awful', 'worst', 'hate', 'poor']
    pos = sum(1 for w in positive_words if w in text_lower)
    neg = sum(1 for w in negative_words if w in text_lower)
    if pos > neg:
        return 'positive'
    elif neg > pos:
        return 'negative'
    else:
        return 'neutral'


@api_view(['GET'])
def get_cars(request):
    makes = CarMake.objects.all()
    result = []
    for make in makes:
        models = []
        for m in make.models.all():
            models.append(m.model)
        result.append({'make': make.make, 'models': models})
    return Response(result)


@api_view(['POST'])
def register(request):
    try:
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        return Response({'message': 'User registered successfully', 'user': {'username': user.username}}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    try:
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful', 'user': {'username': user.username, 'email': user.email}}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_csrftoken(request):
    from django.middleware.csrf import get_token
    return Response({'csrfToken': get_token(request)})


@api_view(['POST'])
def analyze_review(request):
    try:
        data = request.data
        review = data.get('review', '')
        sentiment = analyze_text(review)
        return Response({'sentiment': sentiment})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated:
        return Response({'user': {'username': request.user.username, 'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name}})
    return Response({'user': None})

