from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from rest_framework.decorators import action
from .serializers import FileUploadSerializer, FileGroupUploadSerializer
from .models import File, FileGroup

class FileViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        파일 작업 관련 viewset
    """

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    # 기본 쿼리셋
    queryset = File.objects.all()

    # 사용되는 serializer 클래스
    serializer_classes = {
        'upload_file': FileUploadSerializer,
        'upload_file_group': FileGroupUploadSerializer,
    }

    # 해당 viewset에서 사용되는 기본 권한
    permission_classes = [AllowAny]

    # 파서 클래스 정의 (파일 관련 파서)
    parser_classes = [MultiPartParser, FormParser]

    @action(methods=['POST'], detail=False)
    def upload_file(self, request):
        """
        단일 파일 업로드
        """

        response = self.create(request)
        
        return response


    @action(methods=['POST'], detail=False)
    def upload_file_group(self, request):
        """
        묶음 파일 업로드
        """
        
        response = self.create(request)
        
        return response