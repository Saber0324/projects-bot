import re

CODE_PATTERN = r"```+\s*(?P<language>\S*)\n(?P<code>.*?)```+(?:\n(?P<stdin>[^\n]*))?"


def extract_code(pattern: str, text: str) -> tuple[str, str] | tuple[str, str, str]:
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        if "`" in match.group(2):
            return match.group(1), "tried codeblock escaping"
        if "bf" in match.group(1) or "brainfuck" in match.group(1):
            match_bf = re.search(BF_PATTERN, text, re.DOTALL | re.IGNORECASE)
            if match_bf:
                return match_bf.group(1), match_bf.group(2) + "\n" + match_bf.group(3)
        return match.group(1), match.group(2)
    return "Language unmatched", "No code"
