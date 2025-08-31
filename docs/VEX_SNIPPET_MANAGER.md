# VEX Snippet Manager

A utility for managing and organizing VEX code snippets in Houdini.

## Features

- Organized categories and tags
- Search by name, description, or tags
- Copy to clipboard, edit, and delete
- Persistent storage under your BYVFX package path

## Default Categories

- Attributes — Point, primitive, and vertex attribute manipulation
- Noise Functions — Various noise and turbulence patterns
- Math/Utility — Mathematical operations and utility functions
- Geometry Processing — Geometry manipulation and analysis
- Color/Shading — Color and material related code
- Animation/Time — Time-based and animation effects
- Particles — Particle system related code
- Volumes — Volume manipulation and processing
- Custom — User-defined snippets
- Uncategorized — Default category for unclassified snippets

## File Location

Snippets are stored at:

```text
$BYVFX/scripts/vex_snippets.json
```

If BYVFX is not defined (package not loaded), it falls back to:

```text
$HOUDINI_USER_PREF_DIR/scripts/vex_snippets.json
```

## Usage

### Launching the Manager

- From Shelf Tool: Click "VEX Snippets" on the BYVFX Tools shelf
- From Python Shell:

```python
from byvfx.utils.vex_snippet_manager import show_vex_snippet_manager
show_vex_snippet_manager()
```

- From Script:

```python
exec(open(r"e:\_houdiniFiles\BY_python\byvfx_tools\scripts\launch_vex_snippet_manager.py").read())
```

### Adding Snippets

1. Click "Add Snippet"
2. Choose or create a category
3. Name it, add a description and tags
4. Paste or type your VEX code
5. Click "OK"

### Managing Snippets

- Search using the search bar
- Copy with "Copy to Clipboard"
- Edit via right-click or the "Edit Snippet" button
- Delete via right-click

## Data Structure

```json
{
  "categories": ["Attributes", "Noise Functions", "..."],
  "snippets": {
    "category_name": {
      "snippet_name": {
        "code": "VEX code here",
        "description": "What it does",
        "tags": ["tag1", "tag2"]
      }
    }
  }
}
```

## Programmatic Usage

```python
from byvfx.utils.vex_snippet_manager import VEXSnippetManager, quick_add_snippet

manager = VEXSnippetManager()
quick_add_snippet(
    category="Custom",
    name="My Snippet",
    code="@P.y += sin(@Time) * 0.1;",
    description="Animated vertical wave",
    tags=["animation", "sine", "wave"]
)
```

## Troubleshooting Guide

- Ensure the byvfx_tools package is in your Python path
- Verify PySide2 is available in Houdini
- Check write permissions to the destination folder

 

You can also manage snippets programmatically:

```python
from byvfx.utils.vex_snippet_manager import VEXSnippetManager, quick_add_snippet

# Get manager instance
manager = VEXSnippetManager()

# Add a snippet programmatically
quick_add_snippet(
    category="Custom",
    name="My Snippet",
    code="@P.y += sin(@Time) * 0.1;",
    description="Animated vertical wave",
    tags=["animation", "sine", "wave"]
)

# Search snippets
results = manager.search_snippets("noise")

# Get specific snippet
snippet = manager.get_snippet("Noise Functions", "Turbulent Position")
```

## Tips

1. **Use Descriptive Names**: Make snippet names clear and searchable
2. **Add Tags**: Tags make finding snippets much easier
3. **Include Comments**: Add comments in your VEX code for clarity
4. **Organize by Context**: Use categories that match your workflow
5. **Regular Cleanup**: Periodically review and remove unused snippets

## Troubleshooting

If the VEX Snippet Manager doesn't launch:

1. Ensure the byvfx_tools package is in your Python path
2. Check that you have PySide2 available in Houdini
3. Verify file permissions in your Houdini user preferences directory

## Contributing

To add your own default snippets, modify the `_create_default_data()` method in the `VEXSnippetManager` class.
