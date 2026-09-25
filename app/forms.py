# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, IntegerField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, Regexp

class LoginForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('رمز عبور', validators=[DataRequired(), Length(min=6)])

class RegisterForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=80), Regexp('^[a-zA-Z0-9_]+$', message='فقط حروف انگلیسی، اعداد و زیرخط مجاز است')])
    email = StringField('ایمیل', validators=[DataRequired(), Email(message='ایمیل نامعتبر است')])
    password = PasswordField('رمز عبور', validators=[DataRequired(), Length(min=6, message='رمز عبور حداقل ۶ کاراکتر باید باشد')])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[DataRequired()])
    accept_terms = BooleanField('پذیرش قوانین', validators=[DataRequired(message='باید قوانین را بپذیرید')])

class ProductForm(FlaskForm):
    name = StringField('نام محصول', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('توضیحات', validators=[Optional()])
    price = FloatField('قیمت', validators=[DataRequired(), NumberRange(min=0, message='قیمت باید مثبت باشد')])
    quantity = IntegerField('تعداد موجودی', validators=[Optional(), NumberRange(min=0)])
    category_id = SelectField('دسته‌بندی', validators=[Optional()], coerce=int)
    material = StringField('جنس', validators=[Optional(), Length(max=100)])
    discount_price = FloatField('قیمت با تخفیف', validators=[Optional(), NumberRange(min=0)])
    status = SelectField('وضعیت', validators=[Optional()], choices=[('draft', 'پیش‌نویس'), ('published', 'منتشر شده'), ('archived', 'بایگانی')])
    is_available = BooleanField('موجود است')
    image = FileField('تصویر', validators=[Optional()])
