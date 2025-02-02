import hou

def color_animated_nodes():
    """Colorizes nodes with keyframes in the current network editor."""
    
    network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if not network or not network.currentNode():
        return
    
    parent = network.currentNode().parent()

    animated_nodes = []
    for node in parent.children():
        for parm in node.parms():
            if parm.keyframes():  # Check for actual keyframes
                animated_nodes.append(node)
                break

    if not animated_nodes:
        hou.ui.displayMessage("No animated nodes found")
        return

    user_color = hou.ui.selectColor()
    if user_color is None:
        return

    for node in animated_nodes:
        node.setColor(user_color)