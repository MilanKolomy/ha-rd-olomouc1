with open('/config/themes/glass_dark.yaml', 'r') as f:
    content = f.read()

old = '  bubble-default-backdrop-background-color: "rgba(0, 0, 0, 0.72)"'
new = ('  bubble-default-backdrop-background-color: "rgba(0, 0, 0, 0.72)"\n'
       '  bubble-backdrop-background-color: "rgba(0, 0, 0, 0.72)"')

if old in content:
    content = content.replace(old, new, 1)
    print('Nahrazeno OK')
else:
    # Přidej za bubble-border-radius
    content = content.replace(
        '  bubble-border-radius: "28px"',
        '  bubble-border-radius: "28px"\n  bubble-backdrop-background-color: "rgba(0, 0, 0, 0.72)"',
        1
    )
    print('Přidáno za bubble-border-radius')

with open('/config/themes/glass_dark.yaml', 'w') as f:
    f.write(content)

import yaml
yaml.safe_load(open('/config/themes/glass_dark.yaml'))
print('YAML OK')
