"""
Example: Integrating VEX Snippet Manager with your workflow

This example shows how you can use the VEX Snippet Manager programmatically
to enhance your Houdini workflows.
"""

import hou
from byvfx.utils.vex_snippet_manager import VEXSnippetManager, quick_add_snippet

def setup_default_vex_snippets():
    """
    Add some useful default VEX snippets to your collection.
    Call this function once to populate your snippet library.
    """
    
    # Geometry manipulation snippets
    quick_add_snippet(
        category="Geometry Processing",
        name="Normalize Vector Attribute", 
        code='@v = normalize(@v);',
        description="Normalize a vector attribute",
        tags=["vector", "normalize", "attribute"]
    )
    
    quick_add_snippet(
        category="Geometry Processing",
        name="Remove Points by Group",
        code='if (inpointgroup(0, "delete_me", @ptnum)) {\n    removepoint(0, @ptnum);\n}',
        description="Remove points that belong to a specific group",
        tags=["remove", "points", "group"]
    )
    
    # Advanced noise patterns
    quick_add_snippet(
        category="Noise Functions",
        name="Layered Noise",
        code='float noise1 = noise(@P * 2) * 0.5;\nfloat noise2 = noise(@P * 8) * 0.25;\nfloat noise3 = noise(@P * 32) * 0.125;\n@height = noise1 + noise2 + noise3;',
        description="Multi-octave layered noise for terrain",
        tags=["noise", "layered", "terrain", "height"]
    )
    
    # Color utilities
    quick_add_snippet(
        category="Color/Shading",
        name="HSV Color Space",
        code='vector hsv = rgbtohsv(@Cd);\nhsv.x += 0.1; // Shift hue\n@Cd = hsvtorgb(hsv);',
        description="Convert to HSV, modify, and convert back to RGB",
        tags=["color", "hsv", "hue", "saturation"]
    )
    
    # Animation helpers
    quick_add_snippet(
        category="Animation/Time",
        name="Smooth Oscillation",
        code='float t = sin(@Time * 2 * $PI) * 0.5 + 0.5;\n@P.y += t * chf("amplitude");',
        description="Smooth sine wave oscillation with amplitude control",
        tags=["animation", "sine", "oscillation", "smooth"]
    )
    
    print("Default VEX snippets added successfully!")


def create_vex_wrangle_with_snippet():
    """
    Example function that creates a VEX wrangle node and 
    applies a snippet from the manager.
    """
    
    # Get current network
    network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if not network or not network.currentNode():
        hou.ui.displayMessage("Please navigate to a SOP network")
        return
    
    parent = network.currentNode()
    
    # Create attribwrangle node
    wrangle = parent.createNode("attribwrangle", "vex_snippet")
    
    # Get snippet manager
    manager = VEXSnippetManager()
    
    # Get available snippets
    all_snippets = []
    for category, snippets in manager.snippets_data.items():
        for name in snippets.keys():
            all_snippets.append(f"{category}: {name}")
    
    if not all_snippets:
        hou.ui.displayMessage("No snippets available. Add some snippets first!")
        return
    
    # Let user choose a snippet
    choice = hou.ui.selectFromList(
        all_snippets,
        title="Choose VEX Snippet",
        message="Select a snippet to apply to the wrangle node:"
    )
    
    if choice:
        # Parse the selection
        selected = all_snippets[choice[0]]
        category, name = selected.split(": ", 1)
        
        # Get the snippet
        snippet = manager.get_snippet(category, name)
        if snippet:
            # Apply code to wrangle
            wrangle.parm("snippet").set(snippet["code"])
            
            # Set node comment
            comment = f"VEX Snippet: {name}"
            if snippet.get("description"):
                comment += f"\n{snippet['description']}"
            wrangle.setComment(comment)
            
            # Position and select the node
            wrangle.moveToGoodPosition()
            wrangle.setSelected(True, clear_all_selected=True)
            
            print(f"Applied snippet '{name}' to wrangle node")


def export_snippets_to_hip_file():
    """
    Example function to export all VEX snippets as VEX wrangle nodes
    in the current hip file for backup purposes.
    """
    
    manager = VEXSnippetManager()
    
    # Create a container object
    obj_context = hou.node("/obj")
    container = obj_context.createNode("geo", "vex_snippets_backup")
    
    y_offset = 0
    
    for category, snippets in manager.snippets_data.items():
        # Create category null
        category_null = container.createNode("null", f"CATEGORY_{category}")
        category_null.setPosition([0, y_offset])
        category_null.setComment(f"Category: {category}")
        category_null.setColor(hou.Color(0.8, 0.8, 0.2))
        y_offset -= 1
        
        x_offset = 2
        for name, data in snippets.items():
            # Create wrangle for each snippet
            wrangle = container.createNode("attribwrangle", name.replace(" ", "_"))
            wrangle.setPosition([x_offset, y_offset])
            wrangle.parm("snippet").set(data["code"])
            
            # Set comment with description
            comment = f"Snippet: {name}"
            if data.get("description"):
                comment += f"\n{data['description']}"
            if data.get("tags"):
                comment += f"\nTags: {', '.join(data['tags'])}"
            wrangle.setComment(comment)
            
            x_offset += 3
        
        y_offset -= 2
    
    # Layout the network
    container.layoutChildren()
    
    print(f"Exported {sum(len(snippets) for snippets in manager.snippets_data.values())} snippets to backup container")


if __name__ == "__main__":
    # Example usage
    print("VEX Snippet Manager Integration Examples")
    print("1. setup_default_vex_snippets() - Add default snippets")
    print("2. create_vex_wrangle_with_snippet() - Create wrangle with snippet")
    print("3. export_snippets_to_hip_file() - Export snippets as nodes")
