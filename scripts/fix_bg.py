import re
with open('/config/themes/glass_dark.yaml', 'r') as f:
    c = f.read()
c = re.sub(
    r'lovelace-background:.*',
    'lovelace-background: "linear-gradient(135deg, #0f1230 0%, #3d0e7a 35%, #0e2875 70%, #0f1230 100%)"',
    c
)
with open('/config/themes/glass_dark.yaml', 'w') as f:
    f.write(c)
m = re.search(r'lovelace-background:.*', c)
print(m.group(0))
