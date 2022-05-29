from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    abuse_words = ('IT', 'music', 'science')
    if isinstance(value, str):
        for word in abuse_words:
            value = value.replace(word, '*'*len(word))
        return value
    else:
        raise ValueError(f'Название статьи или текст не являются строковыми')