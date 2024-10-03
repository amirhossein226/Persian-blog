from django.utils.html import format_html
from django.forms.widgets import Media
from tinymce.widgets import TinyMCE


class TinyMceWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class CustomMedia(Media):
    # The reason for customizing Media class is that I need to set the "type" attribute of the js tags(related to quill editor's js files) to "module"
    # actually we could could
    def render_js(self):
        print('The customized render_js method is callleddddddddddd.')
        return [
            (
                path.__html__()
                if hasattr(path, "__html__")
                else format_html('<script src="{}" type="module"></script>', self.absolute_path(path))
            )
            for path in self._js
        ]

    # The default __add__ method of Media using Media() object to combine to media objects,which at the end ,causes to render_js method which we defined above don't call
    def __add__(self, other):
        combined = CustomMedia()
        combined._css_lists = self._css_lists
        combined._js_lists = self._js_lists

        for item in other._css_lists:
            if item and item not in self._css_lists:
                combined._css_lists.append(item)
        for item in other._js_lists:
            if item and item not in self._js_lists:
                combined._js_lists.append(item)
        return combined
