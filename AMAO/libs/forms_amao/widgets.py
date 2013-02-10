# -*- coding: utf-8 -*-
from django.db import models 
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.forms.widgets import ClearableFileInput
 
def change_widget_to_NoFullPathLinkFileInput(f):
    formfield = f.formfield()
    if isinstance(f, models.FileField):
        formfield.widget = NoFullPathLinkFileInput()
    return formfield

class NoFullPathLinkFileInput(ClearableFileInput):
    "new widget that removes the link and full path from a uploaded file, for security"

    # template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)
        if value and hasattr(value, "url"):
            self.template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s'
            value_new = force_unicode(value).split('/')[-1]
            template = self.template_with_initial
            substitutions['initial'] = (u'%s' % escape(value_new))

        return mark_safe(template % substitutions)
