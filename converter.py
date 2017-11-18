# -*- coding: utf-8 -*-

'''
Created on 2016/11/27
Updated on 2017/11/18
__author__ = "Bernardo Gomes de Abreu"
__email__ = "bgomesdeabreu@gmail.com"
'''

import sublime, sublime_plugin
import re


class BaseConvertCommand(sublime_plugin.TextCommand):
    pattern_file = re.compile(r"(.*).py$")
    TO_CLIPBOARD = False

    def run(self, edit):
        print(dir(self.view))
        print(dir(edit))
        self.find_class_and_fields(self.view, edit)

    def is_enabled(self):
        print(dir(sublime))

        return self.view.file_name() is None \
            or re.search(self.pattern_file, self.view.file_name() or "") is not None

    def check_pattern(self, string, patterns):
        for pattern in patterns:
            matchObj = re.match(pattern, string)
            if matchObj:
                return "'" + matchObj.group(1).strip() + "', "
        return ''

    def find_class_and_fields(self, view, edit):
        pattern = re.compile(r"(.*)=(.*)(models.)(.*)(Field)(.*)\)$")
        pattern_fk = re.compile(r"(.*)=(.*)(models.ForeignKey)(.*)\)$")
        pattern_m2m = re.compile(r"(.*)=(.*)(models.ManyToManyField)(.*)\)$")
        pattern_o2o = re.compile(r"(.*)=(.*)(models.OneToOneField)(.*)\)$")
        pattern_class_name = re.compile(r"class(.*)\((.*):$")
        result = ""
        class_name = ''
        for region in view.sel():
            if not region.empty():
                s = view.substr(region)
                for index, string in enumerate(s.split('\n')):
                    if index == 0:
                        class_name = self.check_pattern(string,
                                                        [pattern_class_name])\
                            .replace(', ', '').replace("'", "")
                    result += self.check_pattern(string, [pattern, pattern_fk,
                                                 pattern_m2m, pattern_o2o])
                if self.TO_CLIPBOARD:
                    sublime.set_clipboard(self.BASE_RETURN.format(
                        class_name, result))
                else:
                    view.insert(edit, region.end(), self.BASE_RETURN.format(
                        class_name, result))


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
