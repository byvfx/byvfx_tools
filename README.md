# BYVFX Tools

A collection of production utilities designed to streamline Houdini workflows.

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://linkedin.com/brandoncyoung)
[![Website](https://img.shields.io/badge/Website-BYVFX-green.svg)](https://byvfx.com/)
[![Email](https://img.shields.io/badge/Email-Contact-red.svg)](mailto:brandon@byvfx.com)

</div>

## Core Features

### HDAS
**Draw Points** - draw single point positions in 3D space with customizable markers

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

BYVFX Tools uses Houdini's package system. Choose one of the options below.

### Option A — Point Houdini to this repo's `packages` folder (recommended)

1) Place/clone this repo anywhere (e.g. `E:\yourDirectory\byvfx_tools`).

2) Add the repo's `packages` folder to Houdini's package search path.

3) Restart Houdini. The included `packages/byvfx_package.json` will set:

- BYVFX to the repo root
- HOUDINI_OTLSCAN_PATH to `$BYVFX/otls` (preserving existing with `;&`)
- PYTHONPATH to `$BYVFX/python3.11libs` (preserving existing with `;&`)

### Option B — Copy a package file into your user packages folder

1) Copy `packages/byvfx_package.json` into your user packages directory:

- Windows: `%USERPROFILE%\Documents\Houdini<version>\packages`
- Linux: `~/Houdini<version>/packages`
- macOS: `~/Library/Preferences/houdini/<version>/packages`

1) Edit the copied `byvfx_package.json` so the `BYVFX` env points to your repo path, for example:

```json
{
	"enable": true,
	"load_package_once": true,
	"env": [
		{ "BYVFX": "E:/_houdiniFiles/BY_python/byvfx_tools" },
		{ "HOUDINI_OTLSCAN_PATH": "$BYVFX/otls;&" },
		{ "PYTHONPATH": "$BYVFX/python3.11libs;&" }
	],
	"path": ["$BYVFX"]
}
```

1) Restart Houdini.

### Verify

In Houdini Python Shell:

```python
import hou
print(hou.expandString("$BYVFX"))  # should print your repo path
```

## Usage

Tools are accessible through:

- BYVFX Tools shelf
- Python shell imports from `byvfx.utils` and `byvfx.tools`
- Individual script execution from the scripts directory

## Contact

- Email: [brandon@byvfx.com](mailto:brandon@byvfx.com)
- Website: [byvfx.com](https://byvfx.com)
- LinkedIn: [Connect with me](https://linkedin.com/brandoncyoung)
