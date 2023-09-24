import hou
def convert_mantra_to_redshift(selected_nodes=None):
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