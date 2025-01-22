"""
Alembic Group Splitter Utility for Houdini.

This module provides functionality to split Alembic nodes based on their primitive
groups, creating separate outputs for each group found in the geometry.

author:     brandon young | http://www.byvfx.com
about:      This script splits an alembic node into separate groups if they exist.
"""
import hou
from typing import List, Optional

def get_groups(node: hou.Node) -> List[hou.PrimGroup]:
    """
    Get all primitive groups from an Alembic node.
    
    Args:
        node (hou.Node): The Alembic node to analyze
        
    Returns:
        List[hou.PrimGroup]: List of primitive groups found in the geometry
        
    Raises:
        ValueError: If the node is not a valid Alembic node
    """
    if not node or node.type().name() != "alembic":
        raise ValueError("Please provide a valid Alembic node.")
        
    return node.geometry().primGroups()

def split_by_groups(node: hou.Node) -> List[hou.Node]:
    """
    Split an Alembic node into separate outputs based on primitive groups.
    
    Args:
        node (hou.Node): The Alembic node to split
        
    Returns:
        List[hou.Node]: List of created output nodes
        
    Raises:
        ValueError: If the node has no groups or is invalid
    """
    # Get groups from the node
    groups = get_groups(node)
    if not groups:
        raise ValueError("No groups exist in the selected Alembic node.")
    
    output_nodes = []
    
    # Create outputs for each group
    for group in groups:
        # Create blast node for this group
        blast_node = node.createOutputNode('blast')
        blast_node.parm('group').set(group.name())
        blast_node.parm('negate').set(True)
        
        # Create null output node
        null_node = blast_node.createOutputNode('null', 'OUT_' + group.name())
        output_nodes.append(null_node)
    
    return output_nodes

def show_splitter_ui() -> None:
    """
    Display the ABC Group Splitter interface and handle user interaction.
    This function provides a user interface for splitting Alembic nodes
    based on their primitive groups.
    """
    try:
        # Get selected nodes
        selected = hou.selectedNodes()
        if not selected:
            raise ValueError("No node is selected.")
            
        node = selected[0]
        if node.type().name() != "alembic":
            raise ValueError("Selected node is not an Alembic node.")
            
        # Attempt to split the node
        output_nodes = split_by_groups(node)
        
        # Show success message with group count
        hou.ui.displayMessage(
            f"Successfully created {len(output_nodes)} group outputs.",
            severity=hou.severityType.Message
        )
        
    except ValueError as e:
        # Show error message for expected errors
        hou.ui.displayMessage(
            str(e),
            severity=hou.severityType.Error
        )
    except Exception as e:
        # Show error message for unexpected errors
        hou.ui.displayMessage(
            f"An unexpected error occurred: {str(e)}",
            severity=hou.severityType.Error
        )

if __name__ == "__main__":
    show_splitter_ui()