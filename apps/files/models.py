from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings
from .utils import upload_to_file


class FileGroup(TimeStampedModel):
    """
    묶음 파일 관련 정보
    """

    file_group_id = models.AutoField(primary_key=True)
    class Meta:
        ordering = ['-created']

        verbose_name = '파일 그룹'
        verbose_name_plural = '파일 그룹'


class File(TimeStampedModel):
    """
    파일 업로드 관련 정보

    필드 순서를 바꾸는 것을 권장하지 않음.
    바꿔도 가능한 file 필드가 file_id, file_group을 제외하고 가장 상단에 위치할 수 있도록 유지.

    upload_to_file 함수에서 경로 설정과 동시에 
    instance에 저장할 파일명, 원본 파일명을 설정하는데,
    이때 file가 name, origin_name, file_type, size 보다 하단에 있을 경우
    해당 필드들을 찾지 못해 데이터가 들어가지 않게 된다.

    https://pythonq.com/so/python/481094 
    """

    file_id = models.AutoField(primary_key=True)

    file_group = models.ForeignKey(FileGroup, 
                                    verbose_name="파일 그룹",
                                    null=True, blank=True,
                                    related_name="files",
                                    on_delete=models.SET_NULL)
    
    #TODO: upload 경로는 추후에 필요 시에 변경
    file = models.FileField("저장된 파일 경로 (파일 업로드)", upload_to=upload_to_file, max_length=settings.URL_MAX_LEN)
    
    name = models.CharField("저장된 파일명", max_length=settings.URL_MAX_LEN, editable=False)
    origin_name = models.CharField("원본 파일명", max_length=settings.URL_MAX_LEN, editable=False)
    
    file_type = models.CharField("파일 확장자", max_length=30, editable=False)
    
    size = models.IntegerField("파일 크기", editable=False)
    
    order = models.IntegerField("파일 정렬 순", default=1, null=True, help_text="묶음 파일일 경우 적용됩니다.")

    class Meta:
        ordering = ['-created']

        verbose_name = '파일'
        verbose_name_plural = '파일'

    def __str__(self):
        return f'{self.name} ({self.file})'