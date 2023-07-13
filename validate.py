from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def clean_file(value):
    if not value:
        raise ValidationError(_('Please select a file'))
    
    if not value.lower().endswith('.pdf'):
        raise ValidationError(_('Please select a valid PDF file'))
    
    
    return value