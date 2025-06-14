from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Case, When, Value, IntegerField, F
from .models import Candidate
from .serializers import CandidateSerializer
from functools import reduce
from operator import add


class AtsApiView(APIView):

    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        c_id = request.data.get("id") or request.query_params.get("id")

        if not c_id:
            return Response({"error": "Id not found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            candidate = Candidate.objects.get(pk=c_id)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        candidate_id = request.data.get("id") or request.query_params.get("id")
        if not candidate_id:
            return Response({"error": "Id not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            candidate = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)

        candidate.delete()
        return Response({"message": "Candidate deleted."}, status=status.HTTP_204_NO_CONTENT)


class SearchAPIView(APIView):
    def get(self, request):

        search_query = request.GET.get('q', '').strip()
        if not search_query:
            return Response([])
        query_words = search_query.lower().split()
        name_filter = Q()
        for word in query_words:
            name_filter |= Q(name__icontains=word)

  
        candidates = Candidate.objects.filter(name_filter)


        annotations = {}
        for idx, word in enumerate(query_words):
            annotations[f'match_{idx}'] = Case(
                When(name__icontains=word, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        candidates = candidates.annotate(**annotations)


        match_fields = [F(f'match_{i}') for i in range(len(query_words))]
        if match_fields:
            relevance_score = reduce(add, match_fields)
            candidates = candidates.annotate(relevance=relevance_score)
        else:
            candidates = candidates.annotate(relevance=Value(0, output_field=IntegerField()))
        candidates = candidates.order_by('-relevance', 'name')
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)