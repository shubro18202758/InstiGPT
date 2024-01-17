import re
from bs4 import BeautifulSoup, PageElement
import requests

res = requests.get("https://www.ee.iitb.ac.in/~asethi/students.html")
soup = BeautifulSoup(res.text, "lxml")


def get_content(node: PageElement) -> str:
    name = node.name
    if name is None:
        if str(node) == "\n":
            return " "
        return node.text
    elif name == "a":
        # return get_content(node)
        if node.text != "":
            return f"{node.text} ({node.get('href')}) "
        else:
            text = " ".join([get_content(child) for child in node.children]).replace(
                "\n", ""
            )
            return f"{text} ({node.get('href')}) "
    elif name == "nav" or name == "footer" or name == "img" or name == "svg":
        return ""

    content = ""
    for child in node.children:
        content += get_content(child)

    return content


content = "\n".join([get_content(child) for child in soup.body.children])  # type: ignore
content = re.sub(r"\s{2,}", "\n", content)

with open("temp.txt", "w") as f:
    f.write(content)
