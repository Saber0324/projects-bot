import re

CODE_PATT3: str = (
        r'`{3,}([^\s].*?)\s*\n([\s\S]*?)\n\s*`{3,}'
        )

STDIN_TRIGGER: str = "stdin"

def segregate_code_string(patt: str, text: str) -> dict[str, str, list[str]]:
    result: dict[str, str, list[str]] = {
            "language": "NONE",
            "code": "NONE",
            "stdin": []
            }
    matches = re.findall(patt, text, re.DOTALL)
    # print(matches)
    for lang, body in matches:
        # print(f"Language: : {lang}")
        # print(f"Body: {body}")
        if STDIN_TRIGGER not in lang:
            result["language"] = lang
            result["code"] = body
        elif STDIN_TRIGGER in lang:
            result['stdin'].append(body)
    if len(result["stdin"]) == 0:
        result['stdin'].append("")
    return result

if __name__ == "__main__":
    print("isolated raw testing of parser...")
    test_strings: list[str] = ["""
```python
print("hello world")
c = input("enter any character: ")
print(f"your input character is: {c}")
```    h
""",
                               """
```python



print("hello world")
c = input("enter any character: ")
print(f"your input character is: {c}")
```
        h
""",
                               """
```    python
print("hello world")
c = input("enter any character: ")
print(f"your input character is: {c}")
```
        h
""",
                               """
```python
print("hello world")
c = input("enter any character: ")
print(f"your input character is: {c}")
```
h
                               19:07:15
""",
                               """

                               """,
                               """
```python
print("hello world")
c = input("enter any character: ")
print(f"your input character is: {c}")
```
Now in the illustration we give it input too:
```stdin1
30
```
                               """,
                               """
```python
print("hello world")
c = input("enter any character: ")
print(f"your input character is: {c}")

c = input("enter any character: ")
print(f"your input character is: {c}")

c = input("enter any character: ")
print(f"your input character is: {c}")

```
Now in the illustration we give it input too:
```stdin1
30
```
but there will be more inputs!!!
```stdin2
30
40 50
60 70 80
```
```stdin3
30
```
                               """]

for i in test_strings:
    print(segregate_code_string(CODE_PATT3, i))
