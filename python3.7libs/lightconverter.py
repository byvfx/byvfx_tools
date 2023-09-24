from PySide2 import QtWidgets, QtGui, QtCore
import hou
from BY import redshift_to_mantra_function as redshift_to_mantra
from BY import mantra_to_redshift_function as mantra_to_redshift

class LightConverterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LightConverterDialog, self).__init__(parent)
        
        # Set window title
        self.setWindowTitle("Light Converter")

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Tree Widget to display all lights and their types
        self.lightTreeWidget = QtWidgets.QTreeWidget()
        self.lightTreeWidget.setHeaderLabels(["Light Name", "Type"])
        self.lightTreeWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        layout.addWidget(self.lightTreeWidget)

        # Populate the tree with all lights in the scene
        self.add_lights_recursive(hou.node("/obj"))

        # Buttons to select lights by type
        selectLayout = QtWidgets.QHBoxLayout()

        self.convertToRedshiftButton = QtWidgets.QPushButton("Convert Mantra -> Redshift")
        self.convertToMantraButton = QtWidgets.QPushButton("Convert Redshift -> Mantra")

        self.convertToRedshiftButton.clicked.connect(self.convert_mantra_to_redshift)
        self.convertToMantraButton.clicked.connect(self.convert_redshift_to_mantra)

        self.selectAllMantraButton = QtWidgets.QPushButton("Select All Mantra")
        self.selectAllRedshiftButton = QtWidgets.QPushButton("Select All Redshift")

        self.selectAllMantraButton.clicked.connect(self.select_all_mantra)
        self.selectAllRedshiftButton.clicked.connect(self.select_all_redshift)

        selectLayout.addWidget(self.selectAllMantraButton)
        selectLayout.addWidget(self.selectAllRedshiftButton)

        selectLayout.addWidget(self.convertToRedshiftButton)
        selectLayout.addWidget(self.convertToMantraButton)

        layout.addLayout(selectLayout)

        # Cancel button
        cancelLayout = QtWidgets.QHBoxLayout()
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)
        cancelLayout.addWidget(self.cancelButton)
        layout.addLayout(cancelLayout)


        # Set the main layout
        self.setLayout(layout)


    def add_lights_recursive(self, node):
        """Recursively search for lights in the scene and populate the Tree Widget."""
        light_mapping = {
            "hlight": "Mantra",
            "rslight": "Redshift",
            "envlight": "Mantra",
            "rslightdome": "Redshift"
        }
        main_node_type = node.type().name().split("::")[0]
        if main_node_type in light_mapping:
            item = QtWidgets.QTreeWidgetItem([node.name(), light_mapping[main_node_type]])
            self.lightTreeWidget.addTopLevelItem(item)

        for child_node in node.children():
            self.add_lights_recursive(child_node)
    

    def convert_mantra_to_redshift(self):
        try:
            selected_nodes = [hou.node("/obj/" + item.text(0)) for item in self.lightTreeWidget.selectedItems() if item.text(1) == "Mantra"]
            if not selected_nodes:
                raise Exception("No Mantra lights selected!")
            mantra_to_redshift.convert_mantra_to_redshift(selected_nodes)  # Use the alias before the function
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", str(e))

    def convert_redshift_to_mantra(self):
        try:
            selected_nodes = [hou.node("/obj/" + item.text(0)) for item in self.lightTreeWidget.selectedItems() if item.text(1) == "Redshift"]
            if not selected_nodes:
                raise Exception("No Redshift lights selected!")
            redshift_to_mantra.convert_redshift_to_mantra(selected_nodes)  # Use the alias before the function
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
  
    
    # Use the external function here
    
    def select_all_mantra(self):
        for index in range(self.lightTreeWidget.topLevelItemCount()):
            item = self.lightTreeWidget.topLevelItem(index)
            if item.text(1) == "Mantra":
                item.setSelected(True)
            else:
                item.setSelected(False)

    def select_all_redshift(self):
        for index in range(self.lightTreeWidget.topLevelItemCount()):
            item = self.lightTreeWidget.topLevelItem(index)
            if item.text(1) == "Redshift":
                item.setSelected(True)
            else:
                item.setSelected(False)

def show_light_converter():
    dialog = LightConverterDialog(hou.ui.mainQtWindow())
    dialog.exec_()

# Call the UI
show_light_converter()
