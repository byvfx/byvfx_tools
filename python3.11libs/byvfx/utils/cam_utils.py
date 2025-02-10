# First import the hou module at the module level
import hou

# Define any utility functions or variables you might need
def _get_file_path():
    """
    Helper function to handle file selection dialog.
    Returns the selected file path or None if cancelled.
    """
    return hou.ui.selectFile(
        title="Select Image Sequence",
        file_type=hou.fileType.Image,
        pattern="*.exr *.jpg *.jpeg *.png *.tif *.tiff",
        multiple_select=True,
        image_chooser=False
    )

def getPlates(kwargs):
    """
    Main function to handle plate selection and parameter setting.
    Args:
        kwargs: Dictionary containing Houdini node context information
    """
    # Get the node first - this is crucial as it establishes our context
    node = kwargs['node']
    
    # Get the file path using our helper function
    file_path = _get_file_path()
    
    # Only proceed if we got a path (user didn't cancel)
    if file_path:
        file_path = file_path.strip('"')
        
        # Get and validate our parameter
        plates_parm = node.parm('plates')
        if not plates_parm:
            hou.ui.displayMessage(
                "Error: Could not find 'plates' parameter",
                severity=hou.severityType.Error
            )
            return
            
        # Set our parameter value
        plates_parm.set(file_path)