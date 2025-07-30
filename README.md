# BYVFX Tools

A collection of production utilities designed to streamline Houdini workflows.

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://linkedin.com/brandoncyoung)
[![Website](https://img.shields.io/badge/Website-BYVFX-green.svg)](https://byvfx.com/)
[![Email](https://img.shields.io/badge/Email-Contact-red.svg)](mailto:brandon@byvfx.com)

</div>

## Core Features

### Shelf Tools

**Light Converter** - Convert between different light types with parameter mapping
**Mass Merger** - Merge selected nodes into a single merge node with container options
**VEX Snippet Manager** - Organize and manage VEX code snippets with categories and search
**Camera DB** - Browse and create cameras from the CamDB database with proper sensor settings
**Multi Import** - Import multiple geometry files with automatic switch setup

### Geometry Utilities

**ABC Splitter** - Split Alembic files by path sections with UI selection
**Material Splitter** - Split geometry by material paths into separate blast nodes
**Animated Node Highlighter** - Color nodes with keyframes for visual identification

### File Management

**File Cache Manager** - Manage and edit file cache node paths with grouping system
**Texture Converters** - Arnold and Redshift texture conversion tools with GUI interfaces

### Solaris Integration

**Solaris to OBJ** - Convert Solaris scenes to traditional OBJ networks with material and light translation
**Multi-Renderer Support** - Handle Mantra/Karma, Arnold, and Redshift workflows

## Installation

BYVFX Tools uses Houdini's package management system.

1. Create a `packages` directory in your Houdini preferences:

```bash
# Windows
%USERPROFILE%/Documents/HOUDINIVERSION/packages

# Linux  
~/HOUDINIVERSION/packages

# macOS
~/Library/Preferences/houdini/HOUDINIVERSION/packages
```

2. Create `BYVFX.json` in your packages directory:

```json
{
    "enable": true,
    "env": [
        {"HOUDINI_PATH": "PATH_TO_BYVFX_TOOLS"}
    ]
}
```

3. Restart Houdini to load the package

## Usage

Tools are accessible through:
- BYVFX Tools shelf
- Python shell imports from `byvfx.utils` and `byvfx.tools`
- Individual script execution from the scripts directory

## Contact

- Email: [brandon@byvfx.com](mailto:brandon@byvfx.com)
- Website: [byvfx.com](https://byvfx.com)
- LinkedIn: [Connect with me](https://linkedin.com/brandoncyoung)
