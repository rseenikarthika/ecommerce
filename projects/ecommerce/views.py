from decimal import Decimal

from django.db.models import F, Q, Func, OuterRef, Subquery
from django.db.models.functions import JSONObject, Coalesce
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Products, ProductReview
from .serializers import ProductSerializer, ProductGenericSerializer


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        resDict = {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        }

        return Response(resDict)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductGenericSerializer
        return ProductSerializer

    def get_queryset(self):
        if self.action == "list":
            min_price = Q()
            max_price = Q()
            range_filter = Q()
            brand_filter = Q()
            brand_name_filter = Q()
            category_filter = Q()
            category_name_filter = Q()
            queryset = Products.objects.all()
            ## Sort Search Query
            if "sort_by" in self.request.GET and (self.request.GET['sort_by']).lower() == 'hightolow':
                queryset = queryset.order_by('-price')
            if "sort_by" in self.request.GET and (self.request.GET['sort_by']).lower() == 'lowtohigh':
                queryset = queryset.order_by('price')
            if "sort_by" in self.request.GET and (self.request.GET['sort_by']).lower() == 'newestfirst':
                queryset = queryset.order_by('-id')
            ## Brand Filter Query
            if "brand" in self.request.GET and len(self.request.GET['brand']) > 0:
                brand_filter = Q(brand__id__in=self.request.GET['brand'])
            if "brand_name" in self.request.GET and len(self.request.GET['brand_name']) > 0:
                brand_name_filter = Q(brand__name__icontains=self.request.GET['brand_name'])
            ## Category Filter Query
            if "category" in self.request.GET and len(self.request.GET['category']) > 0:
                category_filter = Q(category__id=self.request.GET['category'])
            if "category_name" in self.request.GET and len(self.request.GET['category_name']) > 0:
                category_name_filter = Q(category__name__icontains=self.request.GET['category_name'])
            ## Price Search Filter
            if "max_price" in self.request.GET and "min_price" in self.request.GET and len(
                    self.request.GET['max_price']) > 0 and len(
                self.request.GET['min_price']) > 0:
                range_filter = Q(price__range=(self.request.GET['min_price'], self.request.GET['max_price']))
            elif "min_price" in self.request.GET and len(self.request.GET['min_price']) > 0:
                min_price = Q(price__lte=self.request.GET['min_price'])
            elif "max_price" in self.request.GET and len(self.request.GET['max_price']) > 0:
                max_price = Q(price__gte=self.request.GET['max_price'])
            query_set = queryset.filter(brand_filter, category_filter, category_name_filter, brand_name_filter,
                                        range_filter, min_price, max_price, deleted=0,
                                        active=1,
                                        category__active=1,
                                        brand__active=1).annotate(
                category_data=JSONObject(id=F('id'), name=F('category__name'), description=F('category__description'),
                                         logo=F('category__logo'),
                                         parent_data=JSONObject(id=F('category__parent'),
                                                                name=F('category__parent__name'),
                                                                description=F('category__parent__description'))),
                brand_data=JSONObject(id=F('id'), name=F('brand__name'), description=F('brand__description'),
                                      logo=F('brand__logo')),
                # review_max_data=Subquery(ProductReview.objects.filter(product=OuterRef('pk')).annotate(
                #     data=Coalesce(Func('max', function='Sum'), Decimal(0))).values('data')
                #                          ),
                review_avg_max_data=Subquery(ProductReview.objects.filter(product=OuterRef('pk')).annotate(
                    data=Coalesce(Func('max', function='Avg'), Decimal(0))).values('data')
                                             ),
            )
            return query_set

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('sort_by', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="Enter 1.Popularity2.Lowtohigh 3.HightoLow 4.NewestFirst"),
        openapi.Parameter('min_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Enter Min Price"),
        openapi.Parameter('max_price', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Enter Max Price"),
        openapi.Parameter('brand', openapi.IN_QUERY, type=openapi.TYPE_ARRAY,
                          items=openapi.Items(type=openapi.TYPE_INTEGER), description="Enter Brand Id"),
        openapi.Parameter('brand_name', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Enter Brand Name"),
        openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Enter Category Id"),
        openapi.Parameter('category_name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                          description="Enter Category Name"),
    ], responses={
        '200': openapi.Response(description="STATUS SUCCESS", examples={
            "application/json": {"status": "string", "message": "string", "more_info": {},
                                 "data": {}}})
    })
    def list(self, request, *args, **kwargs):
        paginator = CustomPagination()
        queryset = paginator.paginate_queryset(self.get_queryset(), request)
        serializer = self.get_serializer_class()(queryset, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
