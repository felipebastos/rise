from djoser.email import ActivationEmail


class MyActivationEmail(ActivationEmail):
    template_name = "rise/activation.html"
