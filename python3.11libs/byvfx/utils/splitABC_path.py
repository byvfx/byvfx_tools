"""
ABC Splitter Utility for Houdini.

This module provides functionality to split Alembic nodes into separate geometries
based on their path attributes.

author:     brandon young | http://www.byvfx.com
date:       2023.07.25
version:    0.6
"""

import hou
import re
from typing import Optional, Set, List, Union

def get_path_sections(node: hou.Node) -> List[Set[str]]:
    """
    Analyze an Alembic node and return all unique path sections at each level.
    
    Args:
        node (hou.Node): The Alembic node to analyze
        
    Returns:
        List[Set[str]]: List of sets containing unique path components at each level
        
    Raises:
        ValueError: If the node has no path attribute
    """
    path_attrib = node.geometry().findPrimAttrib("path")
    if path_attrib is None:
        raise ValueError("The Alembic node does not have a path attribute.")
        
    # Get all prims and their paths
    prims = node.geometry().prims()
    
    # Split paths and collect unique sections at each level
    sections = []
    max_depth = max(len(prim.attribValue(path_attrib).split('/')) 
                   for prim in prims)
                   
    for i in range(max_depth):
        unique_sections = set(
            prim.attribValue(path_attrib).split('/')[i] 
            for prim in prims 
            if len(prim.attribValue(path_attrib).split('/')) > i
        )
        sections.append(unique_sections)
        
    return sections

def split_alembic(node: hou.Node, 
                 section_index: int, 
                 center_and_justify: bool = True) -> List[hou.Node]:
    """
    Split an Alembic node into separate geometries based on path sections.
    
    Args:
        node (hou.Node): The Alembic node to split
        section_index (int): Which path section to split by
        center_and_justify (bool): Whether to add matchsize nodes
        
    Returns:
        List[hou.Node]: List of created output nodes
        
    Raises:
        ValueError: If invalid inputs are provided
    """
    # Validate input node
    if not node or node.type().name() != "alembic":
        raise ValueError("Please provide a valid Alembic node.")
    
    # Get path sections
    sections = get_path_sections(node)
    
    # Validate section index
    if section_index not in range(len(sections)):
        raise ValueError(f"Invalid section index. Must be between 0 and {len(sections)-1}")
    
    # Get unique paths for the chosen section
    unique_paths = sections[section_index]
    output_nodes = []
    
    # Create nodes for each unique path
    for path in unique_paths:
        # Create sanitized node name
        node_name = re.sub(r'\W+', '_', path)
        
        # Create blast node
        blast_node = node.createOutputNode("blast", node_name + "_blast")
        blast_node.parm("group").set('@path=*' + path + '*')
        blast_node.parm("negate").set(1)
        blast_node.setDisplayFlag(True)
        blast_node.setRenderFlag(True)
        
        current_node = blast_node
        
        # Add matchsize if requested
        if center_and_justify:
            match_size = blast_node.createOutputNode(
                "matchsize", 
                node_name + "_matchsize"
            )
            match_size.parm("justify_y").set(1)  # Set Y justify to min
            current_node = match_size
            
        # Create output null
        null_node = current_node.createOutputNode("null", "OUT_" + node_name)
        output_nodes.append(null_node)
        
    return output_nodes

def show_splitter_ui() -> None:
    """
    Display the ABC Splitter interface and handle user interaction.
    """
    # Get selected node
    selected = hou.selectedNodes()
    if not selected:
        raise ValueError("No node selected")
        
    node = selected[0]
    if node.type().name() != "alembic":
        raise ValueError("Selected node is not an Alembic node")
    
    try:
        # Get and display sections
        sections = get_path_sections(node)
        message = "\n".join(
            f"{i}: {section if section else 'Everything'}" 
            for i, section in enumerate(sections)
        )
        
        # Get section choice
        section = hou.ui.readInput(
            "Choose section for splitting:\n" + message,
            buttons=["OK", "Cancel"]
        )
        
        if section[0] == 1 or not section[1].isdigit():
            return
            
        section_index = int(section[1])
        
        # Get center/justify choice
        center_justify = hou.ui.displayMessage(
            "Center and justify objects?",
            buttons=["Yes", "No"],
            default_choice=0,
            close_choice=1,
        )
        
        # Perform the split
        split_alembic(
            node, 
            section_index, 
            center_and_justify=(center_justify == 0)
        )
        
    except Exception as e:
        hou.ui.displayMessage(
            str(e),
            severity=hou.severityType.Error
        )

if __name__ == "__main__":
    show_splitter_ui()