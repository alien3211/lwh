from django import forms
from django.forms.formsets import BaseFormSet

class CmpForm(forms.Form):
    start = forms.FloatField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'start',
                    }),
                    required=False)
    end = forms.FloatField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'end',
                    }),
                    required=False)
    tn = forms.FloatField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'tn',
                    }),
                    required=False)
    tgr = forms.FloatField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'tgr',
                    }),
                    required=False)
    Kn = forms.FloatField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Kn',
                    }),
                    required=False)
    Kgr = forms.FloatField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Kgr',
                    }),
                    required=False)

class LinkForm(forms.Form):
    # cos = forms.CharField(label='Your name', max_length=100)
    # tam = forms.CharField(label='tam', max_length=100)
    # # ToDo: tu masz dodac potrzebne ci parametry plus validacja jak potrzebujesz liczby to liczby a nie stringi

    """
    Form for individual user links
    """
    anchor = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Link Name / Anchor Text',
                    }),
                    required=False)
    url = forms.URLField(
                    widget=forms.URLInput(attrs={
                        'placeholder': 'URL',
                    }),
                    required=False)



# validation data
class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        anchors = []
        urls = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                anchor = form.cleaned_data['anchor']
                url = form.cleaned_data['url']

                # Check that no two links have the same anchor or URL
                if anchor and url:
                    if anchor in anchors:
                        duplicates = True
                    anchors.append(anchor)

                    if url in urls:
                        duplicates = True
                    urls.append(url)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique anchors and URLs.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if url and not anchor:
                    raise forms.ValidationError(
                        'All links must have an anchor.',
                        code='missing_anchor'
                    )
                elif anchor and not url:
                    raise forms.ValidationError(
                        'All links must have a URL.',
                        code='missing_URL'
                    )