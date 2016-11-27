import sublime, sublime_plugin
import re


class BaseConvertCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.find_class_and_fields(self.view, edit)

    def is_enabled(self):
        return True

    def check_pattern(self, string, pattern):
        matchObj = re.match(pattern, string)
        if matchObj:
            return "'" + matchObj.group(1).strip() + "', "
        return ''

    def find_class_and_fields(self, view, edit):
        pattern = re.compile(r"(.*)=(.*)(models.)(.*)(Field)(.*)\)$")
        pattern_class_name = re.compile(r"class(.*)\((.*):$")
        result = "("
        class_name = ''
        for region in view.sel():
            if not region.empty():
                s = view.substr(region)
                for index, string in enumerate(s.split('\n')):
                    if index == 0:
                        class_name = self.check_pattern(string,
                                                        pattern_class_name)\
                            .replace(', ', '').replace("'", "")
                    result += self.check_pattern(string, pattern)
                result += ')'
                view.insert(edit, region.end(), self.BASE_RETURN.format(
                    class_name, result))


class ConvertToSerializer(BaseConvertCommand):
    BASE_RETURN = """

class {}Serializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = {}
    """


class ConvertToModelForm(BaseConvertCommand):
    BASE_RETURN = """

class {}Form(ModelForm):
    class Meta:
        model = Account
        fields = {}
    """
