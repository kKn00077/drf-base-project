from rest_framework import serializers
from .models import File, FileGroup


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file', 'order']
        extra_kwargs = {
            'file': {"allow_empty_file":False, "use_url": True},
            'order': {"required": False, "allow_null": True},
        }


class FileGroupUploadSerializer(serializers.ModelSerializer):
    files = FileUploadSerializer(many=True, required = True)

    def create(self, validated_data):
        """
        request에서 보내는 files 데이터를 serializer files 필드에서 참조
        가져온 files 데이터를 파일 그룹을 생성한 뒤 그 값을 fk로 설정해 DB에 업로드 한다.
        """
        files = validated_data.pop('files')
        group = self.create_file_group()
        
        for file in files:
            File.objects.create(**file, file_group=group)

        return group


    def create_file_group(self):
        return FileGroup.objects.create()

    class Meta:
        model = FileGroup
        fields = '__all__'