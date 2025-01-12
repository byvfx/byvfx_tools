import hou
from typing import List

def mantra_to_redshift(selected_nodes=None):
    """
    Convert Mantra lights in Houdini to Redshift lights.

    Args:
        selected_nodes (list, optional): List of nodes to convert. Defaults to currently selected nodes.
    """
    
    # Parameter mapping from Mantra to Redshift
    param_mapping = {
        "light_intensity": "RSL_intensityMultiplier",
        "light_exposure": "Light1_exposure",
        "env_map": "env_map",
        "light_color": "lightcolor",
        "light_colorr": "light_colorr",
        "light_colorg": "light_colorg",
        "light_colorb": "light_colorb",
        "light_type": "light_type",
        "coneangle": "coneangle",
        "areageometry": "RSL_meshObject",
    }

    # Mapping for the light modes from Mantra to Redshift
    light_mode_mapping = {
        0: 1,
        1: 3,
        2: 3,
        3: 3,
        4: 3,
        5: 3,
        6: 3,
        7: 3,
        8: 0,
    }

    if not selected_nodes:
        selected_nodes = hou.selectedNodes()

    if len(selected_nodes) == 0:
        raise Exception("No node selected")
    else:
        print(f"{len(selected_nodes)} nodes selected.")

    parent_path = None

    for node in selected_nodes:
        # Fetch node type
        main_node_type = node.type().name().split("::")[0]

        #print(f"Processing node {node.name()} of type {main_node_type}.")  # Debug statement

        # Determine the Redshift light type based on Mantra light type
        rs_light_type = "rslight" if main_node_type == "hlight" else "rslightdome" if main_node_type == "envlight" else None

        if rs_light_type:
            #print(f"Determined light type: {rs_light_type}.")  # Debug statement

            # Cache parent node path to minimize repeated calls
            if not parent_path:
                parent_path = node.parent().path()
            
            old_name = node.name()

            # Create a new Redshift Light and inherit the name from the Mantra light
            rs_node = hou.node(parent_path).createNode(rs_light_type, node_name="CONVERTED_" + old_name)
            
            #print(f"Created new Redshift node: {rs_node.name()}.")  # Debug statement

            # Set the new Redshift light's position and move it slightly
            rs_node.setPosition(node.position())
            rs_node.move(hou.Vector2(1, 0))

            # Transfer parameters according to the mapping
            for mantra_param, rs_param in param_mapping.items():
                if node.parm(mantra_param) and rs_node.parm(rs_param):
                     # Set RSL_areashape if light type is 3
                        
                    # If dealing with light type, there's special handling
                    if mantra_param == "light_type":
                        mantra_value = node.parm(mantra_param).evalAsInt()  # Assuming light_type gives an integer value
                    
                        # Set RSL_areashape based on Mantra light type
                        if mantra_value == 3:
                            rs_node.parm("RSL_areaShape").set(1)
                        elif mantra_value == 4:
                            rs_node.parm("RSL_areaShape").set(2)
                        elif mantra_value == 6:
                            rs_node.parm("RSL_areaShape").set(4)
                            rs_node.parm("RSL_meshObject").set(node.parm("areageometry").eval())
                
                        # Check if the Mantra light has cone enabled
                        cone_parm = node.parm("coneenable")
                        cone_enabled = cone_parm.eval() if cone_parm else False
                        
                         # Decide the RS value based on Mantra value and cone status
                        if cone_enabled:
                            rs_value = 2  # Set RS value to 2 if cone is enabled
                        else:
                            rs_value = light_mode_mapping.get(mantra_value, None)  # Fetch from mapping or default to None

                        if rs_value is not None:
                            rs_node.parm(rs_param).set(rs_value)
                            # If cone is enabled, set the RS cone angle
                            if rs_value == 2 and rs_node.parm("coneangle"):
                                rs_node.parm("coneangle").set(node.parm("coneangle").eval())
                        else:
                            print(f"Warning: No mapping found for {mantra_param} value {mantra_value}")

                    # For other parameters, just map directly
                    else:
                        rs_node.parm(rs_param).set(node.parm(mantra_param).eval())
                rs_node.setWorldTransform(node.worldTransform())
                #else:
                   # print(f"Failed to map parameter: {mantra_param} to {rs_param}.")  # Debug statement
        else:
            print(f"Could not determine the Redshift light type for {main_node_type}.")  # Debug statement


def redshift_to_mantra(nodes: List[hou.Node]) -> List[hou.Node]:
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