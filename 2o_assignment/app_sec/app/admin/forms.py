from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, FileField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError
import imghdr


class FileSizeValidator(object):
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, form, field):
        file_size = len(field.data.read())
        field.data.seek(0)  # Reset file position to the beginning

        if file_size > self.max_size:
            raise ValidationError(f'O arquivo é muito grande. O tamanho máximo permitido é {self.max_size / 1024 / 1024} MB.')
        
class ImageFileValidator(object):
    def __init__(self, allowed_extensions=('jpeg', 'png', 'gif')):
        self.allowed_extensions = allowed_extensions

    def __call__(self, form, field):
        file_buffer = field.data.read()
        field.data.seek(0)  # Reset file position to the beginning

        file_extension = imghdr.what(None, h=file_buffer)
        if file_extension not in self.allowed_extensions:
            raise ValidationError(f'Extensão de arquivo não permitida. As extensões permitidas são: {", ".join(self.allowed_extensions)}')



class AddItemForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired(), Length(max=50)])
	price = FloatField("Price:", validators=[DataRequired()])
	category = StringField("Category:", validators=[DataRequired(), Length(max=50)])
	image = FileField("Image:", validators=[DataRequired(), FileSizeValidator(max_size=100 * 1024 * 1024), ImageFileValidator(allowed_extensions=('jpeg', 'png', 'gif'))])  # 100MB max size
	details = StringField("Details:", validators=[DataRequired()])
	price_id = StringField("Stripe id:", validators=[DataRequired()])
	submit = SubmitField("Add")

class OrderEditForm(FlaskForm):
	status = StringField("Status:", validators=[DataRequired()])
	submit = SubmitField("Update")