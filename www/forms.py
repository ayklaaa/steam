from django import forms

from user_profile.models import *
from .models import *
from django.forms import inlineformset_factory

class CommentForm(forms.ModelForm):
    class Meta:
        model = MComment
        fields = ["text"]


class TagSelectionForm(forms.ModelForm):
    class Meta:
        model = Teg
        fields = ['status']



class ReplyForm(forms.ModelForm):
    class Meta:
        model = MReply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Напишите ответ...',
                'rows': 3,
                'class': 'form-control',
            }),
        }


class GameForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=MCategory.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple'}),
        required=True,
        label='Categoty'
    )

    class Meta:
        model = MGame
        fields = ['name', 'category', 'description', 'image', 'video', 'about', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'about': forms.Textarea(attrs={'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'})  # Просто Select без Select2
        }


ImageFormSet = inlineformset_factory(
    parent_model=MGame,
    model=MImage,
    fields=('image',),
    extra=4,
    can_delete=False
)

# class MultipleImageUploadForm(forms.Form):
#     game = forms.ModelChoiceField(queryset=MGame.objects.all(), required=True)
#     images = forms.FileField(widget=forms.FileInput(attrs={"multiple": True}), required=True)
#
#     def clean_images(self):
#         images = self.cleaned_data.get('images')
#         if isinstance(images, list):  # Убедитесь, что это список изображений
#             return images
#         raise forms.ValidationError("Пожалуйста, выберите несколько изображений.")