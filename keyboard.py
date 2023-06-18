import re

text = "/catalog1 is a special text."
table_names = ['embroidery', 'catalog', 'color', 'thread', 'category', 'product', 'category_product', 'buttons']

pattern = r"/\b(" + "|".join(re.escape(word) for word in table_names) + r"\w*)+\d+\b"
print(pattern)
match = re.search(pattern, text)
print(match)
if match:
    print("Match found:", match.group())