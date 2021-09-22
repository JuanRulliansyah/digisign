import mimetypes

import magic
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64FileField


class DocumentBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf', 'jpg', 'jpeg', 'png', 'docx']

    def get_file_extension(self, filename, decoded_file):
        file_type = magic.from_buffer(decoded_file, mime=True)
        if file_type not in ['image/jpeg', 'image/png', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            raise ValidationError(self.INVALID_FILE_MESSAGE)

        extension = mimetypes.guess_extension(file_type)
        return extension.replace('.', '')