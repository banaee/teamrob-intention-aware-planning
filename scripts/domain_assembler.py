# scripts/convert_gazebo_to_env_layout.py
"""

# TODO: this is depricated script, as we are now using now a handcrafted environment layout JSON (not YAML anymore, and it is not called domain anymore)


Convert Gazebo world JSON to env_layout.yaml.
For now, uses hardcoded test data (no Gazebo JSON input yet).
"""

import logging

import yaml
from pathlib import Path

def generate_test_environment_layout():
    """
    Generate test environment layout config.
    TODO: Replace with actual Gazebo JSON parsing when available.
    """
    return {
        'metadata': {
            'name': 'test_kitting_cell',
            'description': 'Test environment for intention recognition',
            'version': '1.0',
            'source': 'hardcoded_test_data'  # Mark as test data
        },
        
        'environment': {
            'width': 1600,
            'height': 800,
            'units': 'pixels'
        },
        
        'zones': [
            {
                'id': 'zone_SE',
                'bounds': {'x_min': 800, 'x_max': 1600, 'y_min': 0, 'y_max': 400},
                'label': 'southeast_storage'
            },
            {
                'id': 'zone_SW',
                'bounds': {'x_min': 0, 'x_max': 800, 'y_min': 0, 'y_max': 400},
                'label': 'southwest_storage'
            },
            {
                'id': 'zone_NW',
                'bounds': {'x_min': 0, 'x_max': 800, 'y_min': 400, 'y_max': 800},
                'label': 'northwest_work'
            },
            {
                'id': 'zone_NE',
                'bounds': {'x_min': 800, 'x_max': 1600, 'y_min': 400, 'y_max': 800},
                'label': 'northeast_work'
            }
        ],
        
        'shelves': [
            {'id': 'shelf_1', 'position': [100, 100], 'size': [100, 100], 'slots': 4, 'zone': 'zone_SW'},
            {'id': 'shelf_2', 'position': [300, 100], 'size': [100, 100], 'slots': 4, 'zone': 'zone_SW'},
            {'id': 'shelf_3', 'position': [1400, 100], 'size': [100, 100], 'slots': 4, 'zone': 'zone_SE'}
        ],
        
        'tables': [
            {'id': 'kitting_table', 'position': [650, 710], 'size': [300, 90], 'zone': 'zone_NW'}
        ],
        
        'doors': [
            {'id': 'south_exit', 'position': [725, 0], 'size': [150, 30], 'function': 'exit'},
            {'id': 'north_entry_A', 'position': [1450, 770], 'size': [150, 30], 'function': 'enter'}
        ],
        
        'items': [
            {'id': 'item_1', 'type': 'part_A', 'initial_container': 'shelf_1', 'size': [25, 25]},
            {'id': 'item_2', 'type': 'part_A', 'initial_container': 'shelf_2', 'size': [25, 25]},
            {'id': 'item_3', 'type': 'part_B', 'initial_container': 'shelf_3', 'size': [25, 25]}
        ]
    }

def convert_gazebo_to_env_layout(gazebo_json_path=None, output_path='configs/env_layout.yaml'):
    """
    Convert Gazebo world JSON to env_layout.yaml.
    
    Args:
        gazebo_json_path: Path to Gazebo JSON export (None = use test data)
        output_path: Where to write env_layout.yaml
    """
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if gazebo_json_path is None:
        logging.info("No Gazebo JSON provided - generating test data")
        env_layout = generate_test_environment_layout()
    else:
        logging.info(f"Parsing Gazebo JSON from {gazebo_json_path}")
        # TODO: Implement actual Gazebo parsing
        raise NotImplementedError("Gazebo JSON parsing not yet implemented")
    
    # Write env_layout.yaml
    with open(output_path, 'w') as f:
        yaml.dump(env_layout, f, default_flow_style=False, sort_keys=False)
    
    logging.info(f"Generated environment layout config at {output_path}")
    
    # Summary
    logging.info(f"\nEnvironment Layout Summary:")
    logging.info(f"  - Shelves: {len(env_layout['shelves'])}")
    logging.info(f"  - Items: {len(env_layout['items'])}")
    logging.info(f"  - Zones: {len(env_layout['zones'])}")
    logging.info(f"  - Grid: {env_layout['environment']['width']}x{env_layout['environment']['height']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate env_layout.yaml configuration')
    parser.add_argument('--input', type=str, default=None,
                       help='Path to Gazebo JSON export (omit for test data)')
    parser.add_argument('--output', type=str, default='configs/env_layout.yaml',
                       help='Output path (default: configs/env_layout.yaml)')
    
    args = parser.parse_args()
    
    convert_gazebo_to_env_layout(
            gazebo_json_path=args.input,
            output_path=args.output
        )

    
    print(f"Environment layout assembly complete. file {args.output} generated.")    
