from django.utils.translation import get_language
from collections.abc import Iterable


def translate(objs):
    """
    Translate one object or many objects (QuerySet, list)
    that have name and description fields with language suffixes.
    """
    lang = get_language() or "en"
    lang_map = {
        "vi": "vi",
        "zh-hant": "zh_hant",
        "zh-hans": "zh_hans",
    }
    suffix = lang_map.get(lang.lower())

    def _translate_single(obj):
        if suffix:
            obj.translated_name = getattr(obj, f"name_{suffix}", None) or obj.name
            obj.translated_description = getattr(obj, f"description_{suffix}", None) or obj.description
        else:
            obj.translated_name = obj.name
            obj.translated_description = obj.description
        return obj

    # Handle multiple (QuerySet, list, tuple, etc.)
    if isinstance(objs, Iterable) and not isinstance(objs, (str, bytes)):
        return [_translate_single(obj) for obj in objs]

    # Handle single object
    return _translate_single(objs)
