import json

FILE_PATH  = "../data/resobin_courses.json"

with open(FILE_PATH) as f:
    docs = json.load(f)

for doc in docs:
    inner_dict = doc.get("doc")
    if(isinstance(inner_dict, str)):
        continue
    title_value = inner_dict.get("title")
    code_value = inner_dict.get("code")
    credits_value = inner_dict.get("credits")
    tags = inner_dict.get("tags")
    inner_dict[code_value] = f"{title_value}"
    inner_dict[title_value] = f"{code_value}"
    inner_dict["name"] = f"The course named {title_value} have course code {code_value} and it is of {credits_value} credits and it is tagged as {tags}"

file_name = '../data/resobin_courses_natural_lang.json'

with open(file_name, 'w') as json_file:
    json.dump(docs, json_file, indent=4)
    print(f"Dictionary exported to '{file_name}' as JSON.")
    print(len(docs))