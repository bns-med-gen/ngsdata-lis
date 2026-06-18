from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
import sys
import os

# Add parent directory to path to import orm.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from orm import Base, Biomaterial, MedicalFiles, MedicalReports, MedicalTests, Patients, TestSamples
from .serializers import (
    BiomaterialSerializer, MedicalFilesSerializer, MedicalReportsSerializer,
    MedicalTestsSerializer, PatientsSerializer, TestSamplesSerializer
)

# Create SQLAlchemy engine and session
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'lis.db')
engine = create_engine(f'sqlite:///{DB_PATH}')


class StandardPagination(PageNumberPagination):
    """Standard pagination for LIS API"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class SQLAlchemyViewSet(viewsets.ViewSet):
    """Base ViewSet for SQLAlchemy models"""
    pagination_class = StandardPagination
    permission_classes = [permissions.IsAuthenticated]
    model_class = None
    serializer_class = None

    def get_queryset(self):
        """Get all records from the model"""
        with Session(engine) as session:
            return session.query(self.model_class).all()

    def list(self, request):
        """List records with pagination"""
        with Session(engine) as session:
            queryset = session.query(self.model_class)
            
            # Apply filters
            for param in request.query_params.keys():
                if param not in ['page', 'page_size', 'search', 'ordering']:
                    if hasattr(self.model_class, param):
                        values = request.query_params.getlist(param)
                        if len(values) > 1:
                            queryset = queryset.filter(getattr(self.model_class, param).in_(values))
                        else:
                            queryset = queryset.filter(getattr(self.model_class, param) == values[0])
            
            # Apply search
            search_term = request.query_params.get('search')
            if search_term:
                # Search in all text columns
                columns = inspect(self.model_class).columns
                search_conditions = []
                for col in columns:
                    if col.type.python_type == str:
                        search_conditions.append(col.contains(search_term))
                if search_conditions:
                    from sqlalchemy import or_
                    queryset = queryset.filter(or_(*search_conditions))
            
            # Apply ordering
            ordering = request.query_params.get('ordering')
            if ordering:
                if ordering.startswith('-'):
                    field = ordering[1:]
                    if hasattr(self.model_class, field):
                        queryset = queryset.order_by(getattr(self.model_class, field).desc())
                else:
                    if hasattr(self.model_class, ordering):
                        queryset = queryset.order_by(getattr(self.model_class, ordering))
            
            total_count = queryset.count()
            
            # Apply pagination
            paginator = self.pagination_class()
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            page_number = request.query_params.get('page', 1)
            
            try:
                page_size = int(page_size)
                page_number = int(page_number)
            except (ValueError, TypeError):
                page_size = self.pagination_class.page_size
                page_number = 1
            
            offset = (page_number - 1) * page_size
            items = queryset.offset(offset).limit(page_size).all()
            
            # Serialize
            serializer = self.serializer_class(items, many=True)
            
            # Calculate pagination info
            total_pages = (total_count + page_size - 1) // page_size
            
            return Response({
                'count': total_count,
                'next': page_number + 1 if page_number < total_pages else None,
                'previous': page_number - 1 if page_number > 1 else None,
                'page_size': page_size,
                'total_pages': total_pages,
                'current_page': page_number,
                'results': serializer.data
            })

    def retrieve(self, request, pk=None):
        """Retrieve a single record"""
        with Session(engine) as session:
            record = session.query(self.model_class).filter_by(**{self.get_pk_field(): pk}).first()
            if not record:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(record)
            return Response(serializer.data)

    def get_pk_field(self):
        """Get the primary key field name"""
        pk = inspect(self.model_class).primary_key
        if pk:
            return pk[0].name
        return 'id'


class BiomaterialViewSet(SQLAlchemyViewSet):
    """ViewSet for Biomaterial (read-only)"""
    model_class = Biomaterial
    serializer_class = BiomaterialSerializer


class MedicalFilesViewSet(SQLAlchemyViewSet):
    """ViewSet for MedicalFiles (read-only)"""
    model_class = MedicalFiles
    serializer_class = MedicalFilesSerializer


class MedicalReportsViewSet(SQLAlchemyViewSet):
    """ViewSet for MedicalReports (read-only)"""
    model_class = MedicalReports
    serializer_class = MedicalReportsSerializer


class MedicalTestsViewSet(SQLAlchemyViewSet):
    """ViewSet for MedicalTests (read-only)"""
    model_class = MedicalTests
    serializer_class = MedicalTestsSerializer


class PatientsViewSet(SQLAlchemyViewSet):
    """ViewSet for Patients (read-only)"""
    model_class = Patients
    serializer_class = PatientsSerializer


class TestSamplesViewSet(SQLAlchemyViewSet):
    """ViewSet for TestSamples (read-only)"""
    model_class = TestSamples
    serializer_class = TestSamplesSerializer

