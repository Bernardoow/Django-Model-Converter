import sublime, sublime_plugin
import re


class BaseConvertCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.findClassAndFields(self.view, edit, self.BASE_RETURN)

    def is_enabled(self):
        return True

    def check_pattern(self, string, pattern):
        matchObj = re.match(pattern, string)
        if matchObj:
            return "'" + matchObj.group(1).strip() + "', "
        return ''

    def findClassAndFields(self, view, edit, BASE_RETURN):
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
                            .replace(', ', '')
                    result += self.check_pattern(string, pattern)
                result += ')'
                view.insert(edit, region.end(), BASE_RETURN.format(
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
