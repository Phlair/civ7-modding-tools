"""
SQL File Import Example

This example demonstrates:
- Importing external SQL database files
- Database modifications for game content
- SQL scripts for data patches and extensions
- Organizing SQL assets in mods
"""

from civ7_modding_tools import Mod
from civ7_modding_tools.builders import ImportFileBuilder

mod = Mod(
    id='sql-import-example',
    version='1.0.0',
    name='SQL Import Example',
    description='Demonstrates importing SQL database files'
)

# Import custom SQL database modifications
sql_import = ImportFileBuilder({
    'source': './assets/custom-civs.sql',
    'target_name': 'data/custom-civs.sql',
})

# Import additional SQL patches
sql_patch = ImportFileBuilder({
    'source': './assets/balance-patch.sql',
    'target_name': 'data/patches/balance.sql',
})

mod.add([sql_import, sql_patch])
mod.build('./dist-sql-example')
print("SQL import example mod built successfully!")
