with open('/config/configuration.yaml', 'r') as f:
    content = f.read()

# Zakomentuj knx řádek
content = content.replace(
    'knx: !include knx-config/knx.yaml',
    '# knx: !include knx-config/knx.yaml  # zakomentovano - KNX neni nainstalovano'
)

# Přidej homeassistant: packages: (pokud tam není)
if 'packages:' not in content:
    content = content.replace(
        '# Loads default set of integrations. Do not remove.\ndefault_config:',
        '# Loads default set of integrations. Do not remove.\ndefault_config:\n\nhomeassistant:\n  packages: !include_dir_named packages'
    )

with open('/config/configuration.yaml', 'w') as f:
    f.write(content)

print('Hotovo. Obsah configuration.yaml:')
print(open('/config/configuration.yaml').read())
