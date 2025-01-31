import hou

def color_animated_nodes():
    """Colorizes nodes with keyframes in the current network editor."""
    user_color = hou.ui.selectColor()
    if user_color is None:
        return

    network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if not network or not network.currentNode():
        return
    
    parent = network.currentNode().parent()

    for node in parent.children():
        for parm in node.parms():
            if parm.keyframes():  # Check for actual keyframes
                node.setColor(user_color)
                break