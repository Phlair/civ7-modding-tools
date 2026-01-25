"""
YAML to Python Converter for Civ7 Modding Tools

Converts a YAML configuration file into a Python script that uses the
civ7_modding_tools library to create a civilization mod.

Usage:
    python yml_to_py.py babylon_civilization.yml -o babylon_generated.py
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


class YamlToPyConverter:
    """Converts YAML mod configuration to Python code."""
    
    def __init__(self, yaml_data: dict[str, Any]):
        """Initialize converter with parsed YAML data."""
        self.data = yaml_data
        self.lines: list[str] = []
        self.indent_level = 0
        self.action_group_var_name: str = 'ALWAYS'  # Default action group variable
        
    def indent(self) -> str:
        """Return current indentation string."""
        return '    ' * self.indent_level
    
    def add_line(self, line: str = '') -> None:
        """Add a line with current indentation."""
        if line:
            self.lines.append(f'{self.indent()}{line}')
        else:
            self.lines.append('')
    
    def format_value(self, value: Any) -> str:
        """Format a Python value for code generation."""
        if isinstance(value, str):
            # Handle variable references like ${metadata.id}
            if value.startswith('${') and value.endswith('}'):
                ref = value[2:-1]
                parts = ref.split('.')
                if parts[0] == 'metadata':
                    return f"mod.mod_id"
                elif parts[0] == 'constants':
                    return parts[1].upper()
            # Use repr() which properly escapes all special characters including newlines
            return repr(value)
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            if not value:
                return '[]'
            # Check if it's a simple list of strings
            if all(isinstance(v, str) for v in value):
                items = ', '.join(repr(v) for v in value)
                return f'[{items}]'
            # Otherwise format as multi-line
            return self.format_list(value)
        elif isinstance(value, dict):
            return self.format_dict(value)
        elif value is None:
            return 'None'
        return str(value)
    
    def format_list(self, lst: list[Any], inline: bool = False) -> str:
        """Format a list as Python code."""
        if not lst:
            return '[]'
        
        if inline:
            items = ', '.join(self.format_value(v) for v in lst)
            return f'[{items}]'
        
        # Multi-line list
        result = '[\n'
        self.indent_level += 1
        for item in lst:
            result += f'{self.indent()}{self.format_value(item)},\n'
        self.indent_level -= 1
        result += f'{self.indent()}]'
        return result
    
    def format_dict(self, dct: dict[str, Any], inline: bool = False) -> str:
        """Format a dictionary as Python code."""
        if not dct:
            return '{}'
        
        if inline and len(dct) <= 2:
            items = ', '.join(f"'{k}': {self.format_value(v)}" for k, v in dct.items())
            return f'{{{items}}}'
        
        # Multi-line dict
        result = '{\n'
        self.indent_level += 1
        for key, value in dct.items():
            formatted_value = self.format_value(value)
            result += f"{self.indent()}'{key}': {formatted_value},\n"
        self.indent_level -= 1
        result += f'{self.indent()}}}'
        return result
    
    def generate_docstring(self) -> None:
        """Generate module docstring."""
        metadata = self.data.get('metadata', {})
        name = metadata.get('name', 'Civilization')
        description = metadata.get('description', '')
        
        self.add_line('"""')
        self.add_line(f'{name} Civilization - Generated from YAML')
        self.add_line()
        self.add_line(description)
        self.add_line('"""')
        self.add_line()
    
    def generate_imports(self) -> None:
        """Generate import statements."""
        self.add_line('from civ7_modding_tools import Mod, ActionGroupBundle')
        self.add_line('from civ7_modding_tools.builders import (')
        self.indent_level += 1
        self.add_line('CivilizationBuilder,')
        self.add_line('UnitBuilder,')
        self.add_line('ConstructibleBuilder,')
        self.add_line('ProgressionTreeBuilder,')
        self.add_line('ProgressionTreeNodeBuilder,')
        self.add_line('ModifierBuilder,')
        self.add_line('ImportFileBuilder,')
        self.add_line('TraditionBuilder,')
        self.indent_level -= 1
        self.add_line(')')
        self.add_line('from civ7_modding_tools.localizations import (')
        self.indent_level += 1
        self.add_line('ModuleLocalization,')
        self.add_line('TraditionLocalization,')
        self.indent_level -= 1
        self.add_line(')')
        self.add_line()
    
    def generate_constants(self) -> None:
        """Generate constant definitions."""
        constants = self.data.get('constants', {})
        if not constants:
            return
        
        self.add_line('# Constants')
        for name, value in constants.items():
            const_name = name.upper()
            if isinstance(value, list):
                self.add_line(f'{const_name} = [')
                self.indent_level += 1
                for item in value:
                    self.add_line(f"'{item}',")
                self.indent_level -= 1
                self.add_line(']')
            else:
                self.add_line(f"{const_name} = {self.format_value(value)}")
        self.add_line()
    
    def generate_module_localization(self) -> None:
        """Generate module localization."""
        mod_loc = self.data.get('module_localization', {})
        if not mod_loc:
            return
        
        self.add_line('# Module localization')
        self.add_line('MODULE_LOC = ModuleLocalization(')
        self.indent_level += 1
        for key, value in mod_loc.items():
            self.add_line(f'{key}="{value}",')
        self.indent_level -= 1
        self.add_line(')')
        self.add_line()
    
    def generate_mod_creation(self) -> None:
        """Generate Mod instance creation."""
        metadata = self.data.get('metadata', {})
        mod_loc = self.data.get('module_localization', {})
        
        self.add_line('# Mod metadata and setup')
        self.add_line('mod = Mod({')
        self.indent_level += 1
        for key, value in metadata.items():
            self.add_line(f"'{key}': {self.format_value(value)},")
        if mod_loc:
            self.add_line("'module_localizations': MODULE_LOC,")
        self.indent_level -= 1
        self.add_line('})')
        self.add_line()
    
    def generate_action_group(self) -> None:
        """Generate action group bundle."""
        action_group_data = self.data.get('action_group')
        if not action_group_data:
            return
        
        # Handle both dict and string formats
        if isinstance(action_group_data, dict):
            action_group = action_group_data.get('action_group_id')
        else:
            action_group = action_group_data
        
        if not action_group:
            return
        
        self.add_line('# Action group')
        var_name = action_group.replace('AGE_', '').title()
        self.action_group_var_name = var_name  # Store for builder methods
        self.add_line(f'{var_name} = ActionGroupBundle(action_group_id=\'{action_group}\')')
        self.add_line()
    
    def generate_imports_builders(self) -> None:
        """Generate import file builders."""
        from pathlib import Path
        import os
        
        imports = self.data.get('imports', [])
        if not imports:
            return
        
        self.add_line('# Icon imports')
        
        for imp in imports:
            builder_id = imp['id']
            source_path = imp['source_path']
            
            # Convert relative paths to absolute
            # If path is relative and starts with generated_icons/, resolve it
            if not source_path.startswith('/') and not source_path.startswith('C:'):
                if 'generated_icons' in source_path:
                    # Make absolute relative to current working directory
                    resolved = str(Path(source_path).resolve())
                    source_path = resolved
            
            # Convert backslashes to forward slashes for Python code
            source_path = source_path.replace('\\', '/')
            
            self.add_line(f'{builder_id} = ImportFileBuilder()')
            self.add_line(f'{builder_id}.action_group_bundle = {self.action_group_var_name}')
            self.add_line(f'{builder_id}.fill({{')
            self.indent_level += 1
            self.add_line(f"'source_path': '{source_path}',")
            self.add_line(f"'target_name': '{imp['target_name']}'")
            self.indent_level -= 1
            self.add_line('})')
            self.add_line()
    
    def generate_modifiers(self) -> None:
        """Generate modifier builders."""
        modifiers = self.data.get('modifiers', [])
        if not modifiers:
            return
        
        self.add_line('# Modifiers')
        for modifier_data in modifiers:
            builder_id = modifier_data['id']
            self.add_line(f'{builder_id} = ModifierBuilder()')
            self.add_line(f'{builder_id}.action_group_bundle = {self.action_group_var_name}')
            
            # Build fill dict
            fill_dict = {}
            if 'modifier_type' in modifier_data:
                fill_dict['modifier_type'] = modifier_data['modifier_type']
            if 'modifier' in modifier_data:
                fill_dict['modifier'] = modifier_data['modifier']
            if 'localizations' in modifier_data:
                fill_dict['localizations'] = modifier_data['localizations']
            
            if fill_dict:
                self.add_line(f'{builder_id}.fill({{')
                self.indent_level += 1
                for key, value in fill_dict.items():
                    formatted_value = self.format_value(value)
                    self.add_line(f"'{key}': {formatted_value},")
                self.indent_level -= 1
                self.add_line('})')
            self.add_line()
    
    def generate_traditions(self) -> None:
        """Generate tradition builders."""
        traditions = self.data.get('traditions', [])
        if not traditions:
            return
        
        self.add_line('# Traditions')
        
        for tradition_data in traditions:
            builder_id = tradition_data['id']
            self.add_line(f'{builder_id} = TraditionBuilder()')
            self.add_line(f'{builder_id}.action_group_bundle = {self.action_group_var_name}')
            
            # Build fill dict
            fill_dict = {k: v for k, v in tradition_data.items() if k not in ['id', 'bindings']}
            
            self.add_line(f'{builder_id}.fill({{')
            self.indent_level += 1
            for key, value in fill_dict.items():
                if key == 'localizations':
                    # Handle TraditionLocalization objects
                    self.add_line(f"'{key}': [")
                    self.indent_level += 1
                    for loc in value:
                        self.add_line('TraditionLocalization(')
                        self.indent_level += 1
                        for loc_key, loc_value in loc.items():
                            self.add_line(f"{loc_key}='{loc_value}',")
                        self.indent_level -= 1
                        self.add_line(')')
                    self.indent_level -= 1
                    self.add_line('],')
                else:
                    formatted_value = self.format_value(value)
                    self.add_line(f"'{key}': {formatted_value},")
            self.indent_level -= 1
            self.add_line('})')
            
            # Handle bindings
            if 'bindings' in tradition_data:
                bindings = tradition_data['bindings']
                binding_list = ', '.join(bindings)
                self.add_line(f'{builder_id}.bind([{binding_list}])')
            
            self.add_line()
    
    def generate_units(self) -> None:
        """Generate unit builders."""
        units = self.data.get('units', [])
        if not units:
            return
        
        self.add_line('# Units')
        
        for unit_data in units:
            builder_id = unit_data['id']
            self.add_line(f'{builder_id} = UnitBuilder()')
            self.add_line(f'{builder_id}.action_group_bundle = {self.action_group_var_name}')
            
            # Build fill dict
            fill_dict = {k: v for k, v in unit_data.items() if k not in ['id', 'bindings']}
            
            self.add_line(f'{builder_id}.fill({{')
            self.indent_level += 1
            for key, value in fill_dict.items():
                formatted_value = self.format_value(value)
                self.add_line(f"'{key}': {formatted_value},")
            self.indent_level -= 1
            self.add_line('})')
            self.add_line()
    
    def generate_constructibles(self) -> None:
        """Generate constructible builders."""
        constructibles = self.data.get('constructibles', [])
        if not constructibles:
            return
        
        self.add_line('# Constructibles')
        
        for constructible_data in constructibles:
            builder_id = constructible_data['id']
            self.add_line(f'{builder_id} = ConstructibleBuilder()')
            self.add_line(f'{builder_id}.action_group_bundle = {self.action_group_var_name}')
            
            # Build fill dict
            fill_dict = {k: v for k, v in constructible_data.items() if k not in ['id', 'bindings']}
            
            self.add_line(f'{builder_id}.fill({{')
            self.indent_level += 1
            for key, value in fill_dict.items():
                formatted_value = self.format_value(value)
                self.add_line(f"'{key}': {formatted_value},")
            self.indent_level -= 1
            self.add_line('})')
            self.add_line()
    
    def generate_progression_tree_nodes(self) -> None:
        """Generate progression tree node builders."""
        nodes = self.data.get('progression_tree_nodes', [])
        if not nodes:
            return
        
        self.add_line('# Progression tree nodes')
        
        for node_data in nodes:
            builder_id = node_data['id']
            self.add_line(f'{builder_id} = ProgressionTreeNodeBuilder()')
            self.add_line(f'{builder_id}.action_group_bundle = {self.action_group_var_name}')
            
            # Build fill dict
            fill_dict = {k: v for k, v in node_data.items() if k not in ['id', 'bindings']}
            
            self.add_line(f'{builder_id}.fill({{')
            self.indent_level += 1
            for key, value in fill_dict.items():
                formatted_value = self.format_value(value)
                self.add_line(f"'{key}': {formatted_value},")
            self.indent_level -= 1
            self.add_line('})')
            
            # Handle bindings
            if 'bindings' in node_data:
                bindings = node_data['bindings']
                binding_list = ', '.join(bindings)
                self.add_line(f'{builder_id}.bind([{binding_list}])')
            
            self.add_line()
    
    def generate_progression_trees(self) -> None:
        """Generate progression tree builders."""
        trees = self.data.get('progression_trees', [])
        if not trees:
            return
        
        self.add_line('# Progression trees')
        
        for tree_data in trees:
            builder_id = tree_data['id']
            self.add_line(f'{builder_id} = ProgressionTreeBuilder()')
            self.add_line(f'{builder_id}.action_group_bundle = {self.action_group_var_name}')
            
            # Build fill dict
            fill_dict = {k: v for k, v in tree_data.items() if k not in ['id', 'bindings']}
            
            self.add_line(f'{builder_id}.fill({{')
            self.indent_level += 1
            for key, value in fill_dict.items():
                formatted_value = self.format_value(value)
                self.add_line(f"'{key}': {formatted_value},")
            self.indent_level -= 1
            self.add_line('})')
            
            # Handle bindings
            if 'bindings' in tree_data:
                bindings = tree_data['bindings']
                binding_list = ', '.join(bindings)
                self.add_line(f'{builder_id}.bind([{binding_list}])')
            
            self.add_line()
    
    def generate_civilization(self) -> None:
        """Generate civilization builder."""
        civ_data = self.data.get('civilization')
        if not civ_data:
            return
        
        self.add_line('# Civilization')
        builder_id = civ_data.get('id', 'civilization')
        
        self.add_line(f'{builder_id} = CivilizationBuilder()')
        self.add_line(f'{builder_id}.action_group_bundle = {self.action_group_var_name}')
        
        # Build fill dict (exclude bindings - they're auto-generated)
        fill_dict = {k: v for k, v in civ_data.items() if k not in ['id', 'bindings']}
        
        self.add_line(f'{builder_id}.fill({{')
        self.indent_level += 1
        for key, value in fill_dict.items():
            formatted_value = self.format_value(value)
            self.add_line(f"'{key}': {formatted_value},")
        self.indent_level -= 1
        self.add_line('})')
        
        self.add_line()
    
    def collect_all_builders(self) -> list[str]:
        """Collect all builder IDs from YAML data."""
        builders = []
        
        # Import file builders
        for imp in self.data.get('imports', []):
            builders.append(imp['id'])
        
        # Modifier builders
        for modifier in self.data.get('modifiers', []):
            builders.append(modifier['id'])
        
        # Tradition builders
        for tradition in self.data.get('traditions', []):
            builders.append(tradition['id'])
        
        # Unit builders
        for unit in self.data.get('units', []):
            builders.append(unit['id'])
        
        # Constructible builders
        for constructible in self.data.get('constructibles', []):
            builders.append(constructible['id'])
        
        # Progression tree node builders
        for node in self.data.get('progression_tree_nodes', []):
            builders.append(node['id'])
        
        # Progression tree builders
        for tree in self.data.get('progression_trees', []):
            builders.append(tree['id'])
        
        return builders
    
    def collect_bound_modifiers(self) -> set[str]:
        """Collect modifier IDs that are already bound to other entities."""
        bound = set()
        
        # Modifiers bound to progression tree nodes
        for node in self.data.get('progression_tree_nodes', []):
            if 'bindings' in node:
                for binding in node['bindings']:
                    bound.add(binding)
        
        # Modifiers bound to traditions
        for tradition in self.data.get('traditions', []):
            if 'bindings' in tradition:
                for binding in tradition['bindings']:
                    bound.add(binding)
        
        return bound
    
    def generate_bindings(self) -> None:
        """Generate automatic bindings for civilization builder."""
        civilization = self.data.get('civilization', {})
        if not civilization:
            return
        
        # Collect modifiers that are already bound elsewhere
        already_bound_modifiers = self.collect_bound_modifiers()
        
        # Collect only the top-level entities that should be bound to civilization
        to_bind = []
        
        # Units
        for unit in self.data.get('units', []):
            to_bind.append(unit['id'])
        
        # Constructibles
        for constructible in self.data.get('constructibles', []):
            to_bind.append(constructible['id'])
        
        # Progression trees
        for tree in self.data.get('progression_trees', []):
            to_bind.append(tree['id'])
        
        # Top-level modifiers (not bound to other entities)
        for modifier in self.data.get('modifiers', []):
            modifier_id = modifier['id']
            if modifier_id not in already_bound_modifiers:
                to_bind.append(modifier_id)
        
        if to_bind:
            self.add_line('# Bind all entities to civilization')
            civ_id = civilization.get('id', 'civilization')
            binding_list = ', '.join(to_bind)
            self.add_line(f'{civ_id}.bind([{binding_list}])')
            self.add_line()
    
    def generate_mod_add(self) -> None:
        """Generate mod.add() calls with all builders."""
        # Collect all builders dynamically
        all_builders = self.collect_all_builders()
        
        # Add civilization at the beginning
        civilization = self.data.get('civilization', {})
        civ_id = civilization.get('id', 'civilization')
        final_builders = [civ_id] + all_builders
        
        if not final_builders:
            return
        
        self.add_line('# Add all builders to mod')
        self.add_line('mod.add([')
        self.indent_level += 1
        for builder in final_builders:
            self.add_line(f'{builder},')
        self.indent_level -= 1
        self.add_line('])')
        self.add_line()
    
    def generate_build_call(self) -> None:
        """Generate mod.build() call."""
        build = self.data.get('build', {})
        output_dir = build.get('output_dir', None)
        
        self.add_line('# Build mod')
        self.add_line("if __name__ == '__main__':")
        self.indent_level += 1
        if output_dir:
            # Use explicit output directory if specified
            self.add_line(f"mod.build('{output_dir}')")
        else:
            # Use dynamic directory based on mod ID
            self.add_line("mod.build(f'./dist-{mod.mod_id}')")
        self.indent_level -= 1
    
    def convert(self) -> str:
        """Convert YAML to Python code."""
        self.generate_docstring()
        self.generate_imports()
        self.generate_constants()
        self.generate_module_localization()
        self.generate_mod_creation()
        self.generate_action_group()
        self.generate_imports_builders()
        self.generate_modifiers()
        self.generate_traditions()
        self.generate_units()
        self.generate_constructibles()
        self.generate_progression_tree_nodes()
        self.generate_progression_trees()
        self.generate_civilization()
        self.generate_bindings()
        self.generate_mod_add()
        self.generate_build_call()
        
        return '\n'.join(self.lines)


def main():
    """Main entry point for the converter."""
    parser = argparse.ArgumentParser(
        description='Convert YAML mod configuration to Python code'
    )
    parser.add_argument(
        'yaml_file',
        type=Path,
        help='Path to the YAML configuration file'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output Python file (default: <yaml_file>_generated.py)'
    )
    
    args = parser.parse_args()
    
    # Check if YAML file exists
    if not args.yaml_file.exists():
        print(f'Error: File not found: {args.yaml_file}', file=sys.stderr)
        sys.exit(1)
    
    # Determine output file
    if args.output is None:
        args.output = args.yaml_file.parent / f'{args.yaml_file.stem}_generated.py'
    
    # Load YAML
    try:
        with open(args.yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
    except Exception as e:
        print(f'Error loading YAML: {e}', file=sys.stderr)
        sys.exit(1)
    
    # Convert
    converter = YamlToPyConverter(yaml_data)
    python_code = converter.convert()
    
    # Write output
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(python_code)
        print(f'Successfully generated: {args.output}')
    except Exception as e:
        print(f'Error writing output: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
