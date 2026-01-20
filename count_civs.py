from civ7_modding_tools.data import get_civilizations

civs = get_civilizations()
by_age = {}
for c in civs:
    age = c.get('age')
    if age not in by_age:
        by_age[age] = []
    by_age[age].append(c['id'])

import json
print(json.dumps(by_age, indent=2))

print(f'\n\nTotals:')
print(f'  Antiquity: {len(by_age.get("AGE_ANTIQUITY", []))}')
print(f'  Exploration: {len(by_age.get("AGE_EXPLORATION", []))}')
print(f'  Modern: {len(by_age.get("AGE_MODERN", []))}')
print(f'  TOTAL: {len(civs)}')
