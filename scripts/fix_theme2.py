with open('/config/themes/glass_dark.yaml', 'r') as f:
    content = f.read()

# Přidej bubble-default-backdrop-background-color na konec Bubble Card bloku
old = '  bubble-border-radius: "28px"'
new = '  bubble-border-radius: "28px"\n  bubble-default-backdrop-background-color: "rgba(0, 0, 0, 0.72)"'

content = content.replace(old, new, 1)

with open('/config/themes/glass_dark.yaml', 'w') as f:
    f.write(content)

import yaml
yaml.safe_load(open('/config/themes/glass_dark.yaml'))
print('YAML OK')
print('Přidáno:', 'bubble-default-backdrop-background-color' in content)
