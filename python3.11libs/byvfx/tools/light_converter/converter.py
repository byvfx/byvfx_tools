from PySide2 import QtWidgets, QtGui, QtCore
import hou
from typing import List, Dict, Optional, Union
from . import mantra, redshift

LIGHT_MAPPING = {
    # Mantra lights
    "hlight": "Mantra",
    "envlight": "Mantra",
    # Redshift lights
    "rslight": "Redshift",
    "rslightdome": "Redshift"
}

def convert_light(node: hou.Node, target_renderer: str) -> Optional[hou.Node]:
    """
    Convert a single light node to a different renderer type.
    
    This function serves as the main programmatic interface for light conversion.
    It can be used directly from Python without going through the UI.
    
    Args:
        node (hou.Node): The Houdini light node to convert
        target_renderer (str): The target renderer ("mantra" or "redshift")
        
    Returns:
        Optional[hou.Node]: The newly created light node, or None if conversion wasn't needed
        
    Raises:
        ValueError: If the node isn't a supported light type or target_renderer is invalid
        
    Example:
        >>> light = hou.node("/obj/hlight1")
        >>> new_light = convert_light(light, "redshift")
    """
    # Normalize the target renderer name
    target_renderer = target_renderer.lower()
    if target_renderer not in ["mantra", "redshift"]:
        raise ValueError(f"Unsupported target renderer: {target_renderer}")
    
    # Get the node's base type
    node_type = node.type().name().split("::")[0]
    
    # Verify this is a supported light type
    if node_type not in LIGHT_MAPPING:
        raise ValueError(f"Node {node.path()} is not a supported light type")
    
    # Get current renderer type
    current_renderer = LIGHT_MAPPING[node_type].lower()
    
    # Skip if already the correct type
    if current_renderer == target_renderer:
        return None
        
    try:
        # Convert based on target
        if target_renderer == "redshift":
            if current_renderer == "mantra":
                return redshift.convert_mantra_to_redshift([node])[0]
        elif target_renderer == "mantra":
            if current_renderer == "redshift":
                return mantra.convert_redshift_to_mantra([node])[0]
    except Exception as e:
        raise RuntimeError(f"Error converting {node.path()}: {str(e)}")

def convert_lights_in_path(path: str, target_renderer: str) -> List[hou.Node]:
    """
    Convert all supported lights under a specific path.
    
    Args:
        path (str): Path to the node containing lights (e.g., "/obj")
        target_renderer (str): Target renderer ("mantra" or "redshift")
        
    Returns:
        List[hou.Node]: List of newly created light nodes
        
    Example:
        >>> new_lights = convert_lights_in_path("/obj", "redshift")
    """
    root = hou.node(path)
    if not root:
        raise ValueError(f"Invalid path: {path}")
    
    new_lights = []
    for node in root.allSubChildren():
        if node.type().name().split("::")[0] in LIGHT_MAPPING:
            try:
                new_light = convert_light(node, target_renderer)
                if new_light:
                    new_lights.append(new_light)
            except Exception as e:
                print(f"Warning: Failed to convert {node.path()}: {str(e)}")
                
    return new_lights

class LightConverterDialog(QtWidgets.QDialog):
    """A dialog for converting lights between different renderers in Houdini."""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(LightConverterDialog, self).__init__(parent)
        self.setWindowTitle("Light Converter")
        self.setup_ui()


    def setup_ui(self) -> None:
        """Initialize and configure all UI elements."""
        # Main layout
        layout = QtWidgets.QVBoxLayout()
        
        # Create and configure the tree widget
        self.setup_tree_widget(layout)
        
        # Create the button layouts
        self.setup_conversion_buttons(layout)
        self.setup_cancel_button(layout)
        
        # Set the main layout
        self.setLayout(layout)
        
        # Populate the tree with lights
        self.populate_lights()

    def setup_tree_widget(self, layout: QtWidgets.QVBoxLayout) -> None:
        """Set up the tree widget for displaying lights."""
        self.lightTreeWidget = QtWidgets.QTreeWidget()
        self.lightTreeWidget.setHeaderLabels(["Light Name", "Type"])
        self.lightTreeWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        layout.addWidget(self.lightTreeWidget)

    def setup_conversion_buttons(self, layout: QtWidgets.QVBoxLayout) -> None:
        """Set up the conversion and selection buttons."""
        button_layout = QtWidgets.QHBoxLayout()

        # Create selection buttons
        self.selectAllMantraButton = QtWidgets.QPushButton("Select All Mantra")
        self.selectAllRedshiftButton = QtWidgets.QPushButton("Select All Redshift")
        self.selectAllMantraButton.clicked.connect(lambda: self.select_all_by_type("Mantra"))
        self.selectAllRedshiftButton.clicked.connect(lambda: self.select_all_by_type("Redshift"))

        # Create conversion buttons
        self.convertToRedshiftButton = QtWidgets.QPushButton("Convert Mantra -> Redshift")
        self.convertToMantraButton = QtWidgets.QPushButton("Convert Redshift -> Mantra")
        self.convertToRedshiftButton.clicked.connect(self.convert_mantra_to_redshift)
        self.convertToMantraButton.clicked.connect(self.convert_redshift_to_mantra)

        # Add buttons to layout
        for button in (self.selectAllMantraButton, self.selectAllRedshiftButton,
                      self.convertToRedshiftButton, self.convertToMantraButton):
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

    def setup_cancel_button(self, layout: QtWidgets.QVBoxLayout) -> None:
        """Set up the cancel button."""
        cancel_layout = QtWidgets.QHBoxLayout()
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)
        cancel_layout.addWidget(self.cancelButton)
        layout.addLayout(cancel_layout)

    def populate_lights(self) -> None:
        """Populate the tree widget with all lights in the scene."""
        self.add_lights_recursive(hou.node("/obj"))

    def add_lights_recursive(self, node: hou.Node) -> None:
        """
        Recursively search for lights in the scene and add them to the tree widget.
        
        Args:
            node (hou.Node): The node to start the recursive search from.
        """
        main_node_type = node.type().name().split("::")[0]
        if main_node_type in LIGHT_MAPPING:
            item = QtWidgets.QTreeWidgetItem([
                node.name(), 
                LIGHT_MAPPING[main_node_type]
            ])
            self.lightTreeWidget.addTopLevelItem(item)

        for child_node in node.children():
            self.add_lights_recursive(child_node)

    def get_selected_nodes(self, renderer_type: str) -> List[hou.Node]:
        """
        Get all selected nodes of a specific renderer type.
        
        Args:
            renderer_type (str): The type of renderer ("Mantra" or "Redshift")
            
        Returns:
            List[hou.Node]: List of selected nodes of the specified type
            
        Raises:
            ValueError: If no lights of the specified type are selected
        """
        selected_nodes = [
            hou.node("/obj/" + item.text(0)) 
            for item in self.lightTreeWidget.selectedItems() 
            if item.text(1) == renderer_type
        ]
        
        if not selected_nodes:
            raise ValueError(f"No {renderer_type} lights selected!")
        
        return selected_nodes

    def convert_mantra_to_redshift(self) -> None:
        """Convert selected Mantra lights to Redshift using the programmatic interface."""
        try:
            selected_nodes = self.get_selected_nodes("Mantra")
            for node in selected_nodes:
                convert_light(node, "redshift")
            self.accept()
        except Exception as e:
            self._show_error(str(e))

    def convert_redshift_to_mantra(self) -> None:
        """Convert selected Redshift lights to Mantra using the programmatic interface."""
        try:
            selected_nodes = self.get_selected_nodes("Redshift")
            for node in selected_nodes:
                convert_light(node, "mantra")
            self.accept()
        except Exception as e:
            self._show_error(str(e))

    def select_all_by_type(self, light_type: str) -> None:
        """
        Select all lights of a specific type.
        
        Args:
            light_type (str): The type of lights to select ("Mantra" or "Redshift")
        """
        for index in range(self.lightTreeWidget.topLevelItemCount()):
            item = self.lightTreeWidget.topLevelItem(index)
            item.setSelected(item.text(1) == light_type)

    def _show_error(self, message: str) -> None:
        """
        Display an error message to the user.
        
        Args:
            message (str): The error message to display
        """
        QtWidgets.QMessageBox.warning(self, "Error", message)


def show_light_converter() -> None:
    """Create and show the light converter dialog."""
    dialog = LightConverterDialog(hou.ui.mainQtWindow())
    dialog.exec_()


if __name__ == "__main__":
    show_light_converter()