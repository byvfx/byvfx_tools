def convert_redshift_to_mantra(selected_nodes=None):
    """
    Convert Redshift lights in Houdini to Mantra lights.

    Args:
        selected_nodes (list, optional): List of nodes to convert. Defaults to currently selected nodes.
    """
    
    # Parameter mapping from Redshift to Mantra
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

    # Mapping for the light modes
    light_mode_mapping = {
        0: 7,
        1: 0,
        2: 0,
        3: 2,
    }

    if not selected_nodes:
        selected_nodes = hou.selectedNodes()

    if len(selected_nodes) == 0:
        raise Exception("No node selected")

    parent_path = None

    for node in selected_nodes:
        # Fetch node type and split version of HDA out
        main_node_type = node.type().name().split("::")[0]

        # Determine the Mantra light type based on the Redshift light type
        mantra_light_type = "hlight" if main_node_type == "rslight" else "envlight" if main_node_type == "rslightdome" else None

        if mantra_light_type:
            # Cache parent node path to minimize repeated calls
            if not parent_path:
                parent_path = node.parent().path()
            
            # Rename the original Redshift light first to avoid naming conflict
            old_name = node.name()
            
            # Create a new Mantra Light and inherit the name from the Redshift light
            mantra_node = hou.node(parent_path).createNode(mantra_light_type, node_name="CONVERTED_" + old_name)
            
            # Set the new Mantra light's position and move it slightly
            mantra_node.setPosition(node.position())
            mantra_node.move(hou.Vector2(1, 0))

            # Transfer parameters according to the mapping
            for rs_param, mantra_param in param_mapping.items():
                if node.parm(rs_param) and mantra_node.parm(mantra_param):
                    # Special handling for dropdowns
                    if rs_param == "light_type":
                        rs_value = node.parm(rs_param).eval()

                        mantra_value = light_mode_mapping.get(rs_value)
                        if mantra_value is not None:
                            mantra_node.parm(mantra_param).set(mantra_value)
                            
                            # Check if the RS Value is 2 and set the coneenable parameter
                            if rs_value == 2:
                                if mantra_node.parm("coneangle"):
                                    mantra_node.parm("coneangle").set(node.parm("coneangle").eval())
                                if mantra_node.parm("coneenable"):
                                    mantra_node.parm("coneenable").set(1)
                        else:
                            print(f"Warning: No mapping found for {rs_param} value {rs_value}")
                    else:
                        mantra_node.parm(mantra_param).set(node.parm(rs_param).eval())
                
                # Match transforms
                mantra_node.setWorldTransform(node.worldTransform())
