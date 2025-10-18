from django import forms

# This form is used in your views.py (function: complete_profile)
# It collects and saves learner profile details including an uploaded image.

class ImageForm(forms.Form):
    profile_picture = forms.ImageField(
        required=False,
        label="Upload Profile Picture"
    )

    # You can extend this form with more fields if needed later
    # Example:
    # phone_no = forms.CharField(max_length=15, required=False)
    # dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __str__(self):
        return "Image Upload Form"

# Keep this alias so your current import in views.py works (since it says `from .forms import imageForm`)
imageForm = ImageForm
