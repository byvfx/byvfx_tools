import hou
from typing import List, Optional

def convert_redshift_to_mantra(nodes: List[hou.Node]) -> List[hou.Node]:
    """
    Convert Redshift lights to Mantra lights. This function is designed to work both
    standalone and when called from the converter UI.

    Args:
        nodes (List[hou.Node]): List of Redshift light nodes to convert.
                               If None, uses currently selected nodes.
        
    Returns:
        List[hou.Node]: List of newly created Mantra light nodes
        
    Raises:
        ValueError: If no valid nodes are provided or if conversion fails
    """
    # First, handle the case where no nodes are provided
    if nodes is None:
        nodes = hou.selectedNodes()
    
    # Validate we have nodes to work with
    if not nodes:
        raise ValueError("No nodes provided for conversion")

    # Define our parameter mappings - this tells us how Redshift parameters
    # correspond to Mantra parameters
    param_mapping = {
        "light_intensity": "light_intensity",
        "RSL_exposure": "light_exposure",
        "RSL_intensityMultiplier": "light_intensity",
        "Light1_exposure": "light_exposure",
        "env_map": "env_map",
        "lightcolor": "light_color",
        "light_colorr": "light_colorr",
        "light_colorg": "light_colorg",
        "light_colorb": "light_colorb",
        "light_type": "light_type",
        "coneangle": "coneangle",
    }

    # Define how Redshift light modes map to Mantra light modes
    light_mode_mapping = {
        0: 7,  # Point light
        1: 0,  # Directional light
        2: 0,  # Spot light
        3: 2,  # Area light
    }

    # This will store our successfully converted nodes
    converted_nodes = []
    
    # Process each node
    for node in nodes:
        try:
            # Get the base node type (strip out any namespacing)
            main_node_type = node.type().name().split("::")[0]

            # Determine which type of Mantra light to create
            if main_node_type == "rslight":
                mantra_light_type = "hlight"
            elif main_node_type == "rslightdome":
                mantra_light_type = "envlight"
            else:
                print(f"Warning: Skipping unsupported node type: {main_node_type}")
                continue

            # Create our new Mantra light
            parent_path = node.parent().path()
            mantra_node = hou.node(parent_path).createNode(
                mantra_light_type,
                node_name="CONVERTED_" + node.name()
            )

            # Position it slightly offset from the original
            mantra_node.setPosition(node.position() + hou.Vector2(1, 0))

            # Copy over all matching parameters
            for rs_param, mantra_param in param_mapping.items():
                # Check both parameters exist before trying to copy
                if node.parm(rs_param) and mantra_node.parm(mantra_param):
                    # Special handling for light type parameter
                    if rs_param == "light_type":
                        rs_value = node.parm(rs_param).eval()
                        mantra_value = light_mode_mapping.get(rs_value)
                        
                        if mantra_value is not None:
                            mantra_node.parm(mantra_param).set(mantra_value)
                            
                            # Extra setup for spotlight type
                            if rs_value == 2:  # If it's a spotlight
                                # Set up cone angle and enable cone
                                if mantra_node.parm("coneangle"):
                                    mantra_node.parm("coneangle").set(
                                        node.parm("coneangle").eval()
                                    )
                                if mantra_node.parm("coneenable"):
                                    mantra_node.parm("coneenable").set(1)
                    else:
                        # For all other parameters, just copy the value
                        mantra_node.parm(mantra_param).set(
                            node.parm(rs_param).eval()
                        )

            # Make sure the new light is in the same place and orientation
            mantra_node.setWorldTransform(node.worldTransform())
            
            # Add this node to our list of successful conversions
            converted_nodes.append(mantra_node)
            
        except Exception as e:
            print(f"Error converting {node.path()}: {str(e)}")
            continue

    # Make sure we actually converted something
    if not converted_nodes:
        raise ValueError("No lights were successfully converted")
        
    return converted_nodes