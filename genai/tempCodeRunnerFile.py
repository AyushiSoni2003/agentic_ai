import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! I am ayushi."
token = enc.encode(text)

print("Tokens : " , token)

decode = enc.decode(token)
print("Decoded : " , decode)