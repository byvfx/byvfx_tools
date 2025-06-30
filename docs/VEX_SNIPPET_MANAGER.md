# VEX Snippet Manager

A comprehensive utility for managing and organizing VEX code snippets in Houdini.

## Features

- **Organized Categories**: Store snippets in predefined or custom categories
- **Search Functionality**: Quickly find snippets by name, description, or tags
- **Rich Metadata**: Add descriptions and tags to snippets for better organization
- **Easy Access**: Copy snippets to clipboard with one click
- **Edit/Delete**: Modify or remove snippets as needed
- **Persistent Storage**: Snippets are saved in your Houdini user preferences

## Default Categories

The VEX Snippet Manager comes with the following predefined categories:

- **Attributes** - Point, primitive, and vertex attribute manipulation
- **Noise Functions** - Various noise and turbulence patterns
- **Math/Utility** - Mathematical operations and utility functions
- **Geometry Processing** - Geometry manipulation and analysis
- **Color/Shading** - Color and material related code
- **Animation/Time** - Time-based and animation effects
- **Particles** - Particle system related code
- **Volumes** - Volume manipulation and processing
- **Custom** - User-defined snippets
- **Uncategorized** - Default category for unclassified snippets

## Usage

### Launching the VEX Snippet Manager

#### From Shelf Tool
1. Add the BYVFX Tools shelf to your Houdini interface
2. Click the "VEX Snippets" tool

#### From Python Shell
```python
from byvfx.utils.vex_snippet_manager import show_vex_snippet_manager
show_vex_snippet_manager()
```

#### From Script
Run the launcher script:
```python
exec(open(r"e:\_houdiniFiles\BY_python\byvfx_tools\scripts\launch_vex_snippet_manager.py").read())
```

### Adding Snippets

1. Click "Add Snippet" button
2. Select or create a category
3. Enter a descriptive name
4. Add a description (optional but recommended)
5. Enter comma-separated tags for easier searching
6. Paste or type your VEX code
7. Click "OK" to save

### Managing Snippets

- **Search**: Use the search bar to find snippets by name, description, or tags
- **Copy**: Select a snippet and click "Copy to Clipboard"
- **Edit**: Right-click a snippet and select "Edit" or use the "Edit Snippet" button
- **Delete**: Right-click a snippet and select "Delete"

### Categories

- **Add Category**: Click "Add Category" to create new categories
- **Custom Categories**: Type a new category name when adding snippets

## Example Snippets Included

The manager comes with several example snippets to get you started:

### Attributes
- Random Color per Point
- Scale by Point Number

### Noise Functions  
- Turbulent Position
- Animated Noise

### Math/Utility
- Distance from Origin
- Remap Values

## File Location

Snippets are stored in:
```
$HOUDINI_USER_PREF_DIR/scripts/vex_snippets.json
```

## Data Structure

Snippets are stored in JSON format with the following structure:

```json
{
  "categories": ["Attributes", "Noise Functions", ...],
  "snippets": {
    "category_name": {
      "snippet_name": {
        "code": "VEX code here",
        "description": "Description of what the code does",
        "tags": ["tag1", "tag2", "tag3"]
      }
    }
  }
}
```

## Programmatic Usage

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
