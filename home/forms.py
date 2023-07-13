from django.core.exceptions import ValidationError
from django.forms import forms
from django.utils.translation import gettext_lazy as _
import magic
import filetype

class PDFForm(forms.Form):
    pdf_file = forms.FileField()



    pdf_file.widget.attrs.update({
        'class':'file-upload-input w3-hide',
        'id':'pdf_file',
        'onchange':'readURL(this);',
        'accept': 'application/pdf'
    })


    def clean_pdf_file(self, *args, **kwargs):
        pdf = self.cleaned_data.get('pdf_file')
        print('PDF=> ', pdf)
        kind = filetype.guess(pdf)
        print('file type =>', kind.mime)
        print('file extension =>', kind.extension)
        if not pdf:
            raise ValidationError(_('Please select a file'))

        if kind.mime != 'application/pdf':
            raise ValidationError(_('Please select a valid PDF file'))

        return pdf