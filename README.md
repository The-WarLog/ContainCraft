# ContainCraft - YAML Builder CLI

## Project Overview

ContainCraft is a command-line interface (CLI) tool designed to simplify the creation, loading, and editing of YAML configuration files. Built with Python and Rich, it provides an interactive, user-friendly experience for managing YAML files with support for multiple predefined schemas including Docker Compose, Kubernetes, Kafka, and custom configurations.

The application implements a complete workflow: CLI input → JSON data model → Tree structure → YAML output, allowing users to build, visualize, and modify YAML configurations with ease.

## Features

- **Interactive YAML Creation**: Build YAML files through guided interactive prompts using predefined schemas.
- **Multiple Schema Support**: 
  - Docker Compose (services, ports, volumes, environment variables)
  - Kubernetes (Deployments and Services)
  - Kafka Configuration
  - Custom YAML Builder (flexible key-value structure)
- **YAML Loading**: Load and display existing YAML files with syntax-highlighted preview.
- **YAML Editing**: Edit YAML files in-process with preview and undo functionality before saving.
- **Tree Visualization**: Display loaded YAML as an indented tree structure for easy navigation.
- **Path-based Navigation**: Access nested YAML values using dot notation (e.g., `services.kafka.environment.KAFKA_BROKER_ID`) the user can save both the absolute and relative path if the path is not mentioned then it defaults to current directory.
- **Rich CLI Interface**: Beautiful, colored output with panels, syntax highlighting, and responsive design.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download the project to your local machine:
```bash
cd E:\API\TerMan\Bless (set your desired path)
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows PowerShell
# or
source venv/bin/activate     # On Linux/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

```bash
python .\CLI.py
```

The CLI will display the main menu with four options:

### Menu Options

**1. Create new YAML**
- Choose a predefined schema (Docker Compose, Kubernetes, Kafka, Custom)
- Follow interactive prompts to input configuration details
- Save the generated YAML file

**2. Load existing YAML**
- Provide path to an existing YAML file
- View the YAML content with syntax highlighting
- Display the configuration as a tree structure

**3. Edit YAML**
- Load an existing YAML file
- Choose from editing actions:
  - Set value at path
  - Append to list
  - Delete key
  - Show available keys
  - Undo last change
  - Preview and save changes
  - Cancel without saving

**4. Exit**
- Close the application

### Examples

#### Creating Docker Compose Configuration

```
1. Run: python .\CLI.py
2. Select: 1 (Create new YAML)
3. Choose: Docker Compose
4. Input service details when prompted
5. Save as: docker-compose.yaml
```

#### Editing YAML File

```
1. Select: 3 (Edit YAML)
2. Enter path: new.yaml
3. Choose: 4 (Show available keys)
4. Explore structure
5. Choose: 1 (Set value at path)
6. Enter full path: services.kafka.environment.KAFKA_BROKER_ID
7. Enter new value: 2
8. Choose: 6 (Preview and save)
9. Confirm save
```

## Project Structure

```
ContainCraft/
├── CLI.py                      # Main entry point
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── core/                       # Core data structures and utilities
│   ├── json_model.py          # JSON data model
│   ├── renderer.py            # Tree rendering functionality
│   ├── yaml_io.py             # YAML read/write operations
│   ├── yaml_node.py           # Tree node structure
│   └── yaml_tree.py           # Tree management
├── schemas/                    # YAML schema definitions
│   ├── base_schema.py         # Abstract base schema
│   ├── docker_schema.py       # Docker Compose schema
│   ├── k8s_schema.py          # Kubernetes schema
│   ├── kafka_schema.py        # Kafka configuration schema
│   └── custom_schema.py       # Custom YAML builder schema
├── ui/                         # User interface components
│   ├── inputs.py              # Input handler (prompts, validation)
│   ├── menu.py                # Main menu and workflow management
│   └── tree_viewer.py         # Tree visualization
├── edit/                       # YAML editing functionality
│   └── edit_yaml.py           # In-process editor with preview
└── yaml_cli/                   # CLI utilities
  └── banner.py              # ASCII banner display
```

## Core Components

### YAML Processing Pipeline

The application follows a structured pipeline for YAML processing:

1. **Input**: User provides data through interactive CLI prompts
2. **JSON Model**: Data is stored as a dictionary structure
3. **Tree Structure**: JSON is converted to a tree representation using `YamlNode` and `YamlTree`
4. **Output**: Tree is converted back to dictionary and saved as YAML file

### Data Structures

#### YamlNode
Represents a single node in the YAML tree with:
- `key`: Node identifier
- `value`: Leaf node value (primitive types)
- `children`: List of child nodes

#### YamlTree
Manages the tree structure with methods for:
- Loading dictionary to tree (`load_from_dict`)
- Converting tree to dictionary (`tree_to_dict`)
- Converting dictionary to tree (`dict_to_tree`)
- Handling virtual roots for multi-key YAML files

### Schema System

Each schema extends `BaseSchema` abstract class and implements:
- `guide_user_input(ui)`: Interactive user input to collect data
- `validate(data)`: Validation of collected data
- `default_structure()`: Default template structure

#### Schema Details

**Docker Compose Schema**
- Supports multiple services with individual configurations
- Collects: image, ports, volumes, environment variables, restart policy
- Output: Valid Docker Compose v3 YAML

**Kubernetes Schema**
- Supports Deployment and Service resources
- Collects: API version, kind, metadata, specifications
- Output: Valid Kubernetes YAML manifests

**Kafka Schema**
- Broker configuration management
- Collects: broker IDs, listeners, log directories, environment variables
- Output: Kafka broker configuration

**Custom Schema**
- Free-form YAML builder for non-standard configurations
- Supports: strings, numbers, lists, nested objects
- Output: Fully customizable YAML structure

### Input Handler

Provides reusable input methods:
- `get_string()`: Single-line text input
- `get_number()`: Integer input with min/max validation
- `get_yes_no()`: Boolean confirmation
- `get_choice()`: Selection from list
- `get_list()`: Comma-separated list input
- `get_key_value_pairs()`: Dictionary input
- `get_path_existing()`: File path with validation

### YAML Editor

In-process editor (`edit_yaml.py`) features:
- Non-destructive editing with undo per action
- Path-based value setting with full path notation
- List append operations
- Key deletion
- Interactive key discovery
- Before/after preview with syntax highlighting
- Automatic rollback on errors

## Technical Specifications

### YAML Output Format

The application generates YAML with the following formatting:
- Block style lists (using dashes `-`)
- No sorted keys (maintains input order)
- Proper indentation (2 spaces)
- Proper type handling (lists, dicts, strings, numbers)

Example output:
```yaml
version: '3'
services:
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    ports:
    - 9092:9092
    - 29092:29092
    volumes:
    - /data:/var/lib/kafka/data
    environment:
      KAFKA_BROKER_ID: '1'
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    restart: always
```

### Path Notation

Access nested values using dot notation:
- Simple keys: `services`
- Nested keys: `services.kafka.environment`
- Leaf values: `services.kafka.environment.KAFKA_BROKER_ID`
- List indices: `arr[0].field` (future support)

### Type System

The application preserves data types:
- Strings: Text values with automatic quoting in YAML
- Numbers: Integer values
- Lists: Ordered collections with dash notation
- Dicts: Key-value pairs with proper nesting
- Null: Represented as empty lists `[]` or dicts `{}`

## Dependencies

- **rich** (>=13.0.0): Rich text and formatting in the terminal
- **pyyaml** (>=6.0): YAML parsing and generation
- **blessed** (>=1.20.0): Terminal capability detection (legacy)

See `requirements.txt` for complete dependency list with versions.

## File Operations

### Supported Extensions

- `.yaml`: Standard YAML files
- `.yml`: Alternative YAML extension

### File Handling

- **Load**: Application reads and parses existing YAML files
- **Create**: New YAML files are generated from user input
- **Edit**: Existing files are modified in-process and saved
- **Save**: Files are saved with proper formatting and validation
- **Path Validation**: Ensures provided file paths exist for loading and are valid for saving

### Error Handling

The application includes error handling for:
- Invalid file paths
- Malformed YAML syntax
- Invalid path navigation during editing
- Type mismatches in value assignment
- Missing required keys

## Development Notes

### Design Patterns

1. **Schema Pattern**: Abstract base schema with concrete implementations
2. **Tree Pattern**: Tree-based representation of hierarchical YAML
3. **Command Pattern**: Menu-driven action selection
4. **Factory Pattern**: Schema instantiation based on user selection

### Code Organization

- **Separation of Concerns**: UI, schemas, and core logic are separated
- **Type Hints**: Python type annotations for clarity
- **Abstract Classes**: BaseSchema enforces interface contract
- **Immutability**: Working copies prevent accidental modifications

### Testing Recommendations

1. Create YAML with each schema type
2. Load and verify YAML output format
3. Edit YAML and verify changes persist
4. Test edge cases (empty lists, special characters, deep nesting)
5. Validate against production tools (docker-compose, kubectl)

## Production Readiness

This application is designed for production use cases including:
- Creating Docker Compose files for containerized deployments
- Generating Kubernetes manifests for orchestration
- Managing Kafka broker configurations
- Building custom YAML configurations

### Validation

Before deploying generated YAML files:
1. Verify with appropriate validation tools:
  - Docker Compose: `docker-compose config` (see compose file reference: https://docs.docker.com/compose/compose-file/)
  - Kubernetes: `kubectl apply --dry-run=client` (kubectl reference: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands/#apply)
  - Kafka: Broker configuration reference: https://kafka.apache.org/documentation/#configuration

2. Review configuration values for security and correctness
3. Test in staging environment before production deployment

## Troubleshooting

### Common Issues

**Issue**: Path not found when loading YAML
- **Solution**: Use absolute paths or relative paths from the working directory

**Issue**: Changes not visible after editing
- **Solution**: Ensure option 6 (Preview and save) is selected and confirmed with 'y'

**Issue**: Invalid YAML generated
- **Solution**: Verify input values don't contain special characters requiring escaping

**Issue**: TypeError in path navigation
- **Solution**: Verify full path is correct and values exist; use option 4 to explore structure

## Contributing Guidelines

When extending this project:
1. Maintain the existing code structure and organization
2. Add type hints to new functions
3. Follow naming conventions (snake_case for functions, PascalCase for classes)
4. Update this README for new features
5. Test thoroughly before deployment

## License

This project is provided as-is for educational and commercial use.

## Support and Maintenance

For issues or questions:
1. Review the examples section above
2. Check the troubleshooting section
3. Verify input against schema requirements
4. Consult official documentation for target formats (Docker, Kubernetes, Kafka)

---
