from django import forms
 

class TicketChatForm(forms.Form):
    message = forms.CharField(
        required=True,
        label="پیام ... ",
        widget=forms.Textarea(
            attrs={
                'class':'form-control-custom',
                'placeholder':'پیام خود را بنویسید...',
                'rows':"1"
            }
        )
    )