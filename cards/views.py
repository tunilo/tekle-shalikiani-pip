from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Card
from .serializers import CardSerializer, CardValidationSerializer
import math


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        validation_serializer = CardValidationSerializer(data=request.data)
        validation_serializer.is_valid(raise_exception=True)
        card_number = validation_serializer.validated_data['card_number']
        ccv = validation_serializer.validated_data['ccv']

        is_valid = self.validate_card(card_number, ccv)

        censored_number = f"{card_number[:4]}{'*' * 8}{card_number[-4:]}"

        card = Card.objects.create(
            user=request.user,
            title=request.data.get('title'),
            censored_number=censored_number,
            is_valid=is_valid
        )

        serializer = self.get_serializer(card)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def validate_card(self, card_number, ccv):
        pairs = [(int(card_number[i:i+2]), int(card_number[i+2:i+4])) for i in range(0, len(card_number), 4)]
        for x, y in pairs:
            y1 = y
            x1 = 1
            while y1 > 0:
                x1 = (x1 * x) % ccv 
                y1 -= y
            if x1 % 2 != 0:
                return False
                
        return True
