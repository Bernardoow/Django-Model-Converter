# -*- coding: utf-8 -*-
import re


class Converter(object):
    """docstring for Converter"""

    _PATTERN_CLASS_NAME = re.compile(r"class(?P<class_name>.*)\((.*):$")

    _PATTERN_SIMPLE_FIELD = re.compile(r"(?P<field>.*)=(.*)(models.)(.*)(Field)(.*)\)$")
    _PATTERN_CUSTOM_FIELD = re.compile(r"(?P<field>.*)=(.*)(.*)(Field)(.*)\)$")
    _PATTERN_FK = re.compile(r"(?P<field>.*)=(.*)(models.ForeignKey)(.*)\)$")
    _PATTERN_M2M = re.compile(r"(?P<field>.*)=(.*)(models.ManyToManyField)(.*)\)$")
    _PATTERN_O2O = re.compile(r"(?P<field>.*)=(.*)(models.OneToOneField)(.*)\)$")

    _PATTERNS = [_PATTERN_SIMPLE_FIELD,
                 _PATTERN_CUSTOM_FIELD,
                 _PATTERN_FK,
                 _PATTERN_M2M,
                 _PATTERN_O2O]

    def __init__(self, code):
        super(Converter, self).__init__()
        self.code = code

    def _check_pattern(self, string, patterns):
        for pattern in patterns:
            match_obj = re.match(pattern, string)
            if match_obj:
                return "'" + match_obj.group('field').strip() + "'"
        return ''

    def _split_model_in_small_piece_text_code(self):
        models_str = []
        set_empty_model = ""
        new_model = set_empty_model

        for phrase in self.code.split("\n"):
            new_model += phrase
            if (new_model.count('(') + new_model.count(')')) % 2 == 0:
                new_model = new_model.replace(" ", "")
                if new_model:
                    models_str.append(new_model)
                new_model = set_empty_model
        return models_str

    def _check_pattern_in_model_string(self, list_models_str):
        result = []
        for model_str in list_models_str:
            result.append(self._check_pattern(model_str, self._PATTERNS))

        result = filter(lambda i: len(i) > 0, result)
        return ', '.join(result)

    def get_fields(self):
        models_str = self._split_model_in_small_piece_text_code()
        return self._check_pattern_in_model_string(models_str)

    def get_class_name(self):
        for phrase in self.code.split("\n"):
            match_obj = re.match(self._PATTERN_CLASS_NAME, phrase)
            if match_obj:
                return match_obj.group('class_name').strip()
        return ""
