with open('/config/themes/glass_dark.yaml', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'ha-card-box-shadow: "none"' in line:
        new_lines.append('\n')
        new_lines.append('  # Bubble Card popup - dark theme (CSS vars applied to :root)\n')
        new_lines.append('  bubble-pop-up-background-color: "rgba(15, 17, 23, 0.93)"\n')
        new_lines.append('  bubble-secondary-background-color: "rgba(20, 22, 35, 0.88)"\n')
        new_lines.append('  bubble-pop-up-border: "0.5px solid rgba(255, 255, 255, 0.11)"\n')
        new_lines.append('  bubble-pop-up-border-radius: "28px"\n')
        new_lines.append('  bubble-border: "0.5px solid rgba(255, 255, 255, 0.11)"\n')
        new_lines.append('  bubble-border-radius: "28px"\n')
        break

with open('/config/themes/glass_dark.yaml', 'w') as f:
    f.writelines(new_lines)

import yaml
yaml.safe_load(open('/config/themes/glass_dark.yaml'))
print('YAML OK, lines:', len(new_lines))
