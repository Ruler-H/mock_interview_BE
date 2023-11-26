from django.core.exceptions import ValidationError

def validate_file_size(file):
    if file.size > 1024 * 1024:  # 1MB 이상인 경우
        raise ValidationError("파일 크기가 너무 큽니다. 1MB 이하의 파일을 업로드해주세요.")