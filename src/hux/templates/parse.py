import re

CODE_PATTERN = r"```+\s*(?P<language>\S*)\n(?P<code>.*?)```+(?:\n(?P<stdin>[^\n]*))?"


def extract_code(pattern: str, text: str) -> dict[str, str]:
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        if "`" in match.group(2):
            return {"lang": match.group(1), "code": "Tried codeblock escaping"}
        print(match.groupdict())
        return match.groupdict()
    return {"lang": "Language unmatched", "code": "No code"}
