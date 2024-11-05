__all__ = [
    "safe_format"
]

import re

def safe_format(text, replacements, pattern=r'\{([a-zA-Z0-9_]+)\}', strict=False):
    matches = set(re.findall(pattern, text))
    if strict and (missing := matches - set(replacements.keys())):
        raise ValueError(f"Missing replacements for: {', '.join(missing)}")

    for match in matches & set(replacements.keys()):
        text = re.sub(r'\{' + match + r'\}', str(replacements[match]), text)
    return text


