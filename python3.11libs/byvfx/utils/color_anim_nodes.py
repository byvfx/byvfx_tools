import hou

def color_animated_nodes():
    # Get color from user
    user_color = hou.ui.selectColor()
    if user_color is None:
        return

    # Get current node and its parent
    network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if not network or not network.currentNode():
        return
    
    parent = network.currentNode().parent()

    # Color the animated nodes
    for node in parent.children():
        for parm in node.parms():
            if parm.isTimeDependent():
                node.setColor(user_color)
                break