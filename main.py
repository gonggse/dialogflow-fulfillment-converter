import message_converter 

file_path = "./data/line_faq.json"

content = message_converter.Converter(file_path).to_facebook_message(type="json")

with open(f"facebook_example.json", "w") as outfile:
    outfile.write(content)

print(content)