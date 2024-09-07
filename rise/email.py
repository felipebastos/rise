from djoser.email import ActivationEmail


class ActivationEmail(ActivationEmail):
    template_name = "rise/activation.html"
