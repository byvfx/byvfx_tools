import hou
import os

def show_multi_import():
    """Show the multi-import dialog and create geometry setup."""
    # === UI: Ask user to select multiple files ===
    selected_files = hou.ui.selectFile(
        start_directory="",
        title="Select Geometry Files (.bgeo, .vdb)",
        collapse_sequences=False,
        multiple_select=True,
        file_type=hou.fileType.Any
    )

    # Early exit if user cancels
    if not selected_files:
        raise hou.UserWarning("No files selected.")

    # Sanitize and normalize paths (Windows fix)
    file_list = [f.strip().replace("\\", "/") for f in selected_files.split(";")]

    # === Create GEO container ===
    geo_node = hou.node("/obj").createNode("geo", "geo_import_switch", run_init_scripts=False)
    geo_node.moveToGoodPosition()

    # Clear default file node
    for child in geo_node.children():
        child.destroy()

    # === Create File SOPs ===
    file_nodes = []
    for idx, file_path in enumerate(file_list):
        file_node = geo_node.createNode("file", f"file_{idx}")
        file_node.parm("file").set(file_path)
        file_node.moveToGoodPosition()
        file_nodes.append(file_node)

    # === Create Switch SOP ===
    switch_node = geo_node.createNode("switch", "geo_switch")
    switch_node.moveToGoodPosition()

    # Wire all file nodes into switch
    for i, fn in enumerate(file_nodes):
        switch_node.setInput(i, fn)

    # === Layout ===
    geo_node.layoutChildren()

# For backward compatibility with direct script execution
if __name__ == "__main__":
    show_multi_import()
