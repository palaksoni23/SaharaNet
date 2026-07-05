content = open('app.py', encoding='utf-8').read()

old = '''    response = client.models.generate_content('''

new = '''    import time
    time.sleep(5)
    response = client.models.generate_content('''

result = content.replace(old, new)
if result == content:
    print("ERROR: Match nahi hua!")
else:
    open('app.py', 'w', encoding='utf-8').write(result)
    print("Done!")