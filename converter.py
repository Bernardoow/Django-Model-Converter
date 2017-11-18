# -*- coding: utf-8 -*-

'''
Created on 2016/11/27
Updated on 2017/11/18
__author__ = "Bernardo Gomes de Abreu"
__email__ = "bgomesdeabreu@gmail.com"
'''

import sublime, sublime_plugin
import re

from src.converter import Converter


class BaseConvertCommand(sublime_plugin.TextCommand):
    pattern_file = re.compile(r"(.*).py$")
    TO_CLIPBOARD = False

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                s = self.view.substr(region)
                converter = Converter(s)
                if self.TO_CLIPBOARD:
                    sublime.set_clipboard(self.BASE_RETURN.format(
                        converter.get_class_name(), converter.get_fields()))
                else:
                    self.view.insert(edit, region.end(), self.BASE_RETURN.format(
                        converter.get_class_name(), converter.get_fields()))

    def is_enabled(self):
        return self.view.file_name() is None \
            or re.search(self.pattern_file, self.view.file_name() or "") is not None


class BaseConvertToClipboardCommand(BaseConvertCommand):
    TO_CLIPBOARD = True


class ConvertToSerializer(BaseConvertCommand):
    BASE_RETURN = """

class {0}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {0}
        fields = ({1})
    """


class ConvertToModelForm(BaseConvertCommand):
    BASE_RETURN = """

class {0}Form(ModelForm):
    class Meta:
        model = {0}
        fields = ({1})
    """


class ConvertToFilter(BaseConvertCommand):
    BASE_RETURN = """

class {0}Filter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = {0}
        fields = [{1}]
    """


class ConvertToSerializerClipboard(ConvertToSerializer, BaseConvertToClipboardCommand):
    pass


class ConvertToModelFormClipboard(ConvertToModelForm, BaseConvertToClipboardCommand):
    pass


class ConvertToFilterClipboard(ConvertToFilter, BaseConvertToClipboardCommand):
    pass
