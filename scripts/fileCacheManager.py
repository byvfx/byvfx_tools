from PySide2 import QtWidgets
import hou

def get_filecache_nodes():
    filecache_nodes = []
    for node in hou.node("/").allSubChildren():
        if node.type().name().startswith("filecache"):
            filecache_nodes.append(node)
    return filecache_nodes

class FileCacheNodeEditor(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(FileCacheNodeEditor, self).__init__(parent)
        self.setWindowTitle("File Cache Node Editor")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Node Name', 'Path'])
        self.table.doubleClicked.connect(self.edit_path_in_table)
        self.layout.addWidget(self.table)

        self.update_table()

    def update_table(self):
        filecache_nodes = get_filecache_nodes()
        self.table.setRowCount(len(filecache_nodes))

        for idx, node in enumerate(filecache_nodes):
            self.table.setItem(idx, 0, QtWidgets.QTableWidgetItem(node.name()))
            self.table.setItem(idx, 1, QtWidgets.QTableWidgetItem(node.parm("file").eval()))

        self.adjust_sizes()

    def edit_path_in_table(self, index):
        if index.column() == 1:
            selected_row = index.row()
            node_name = self.table.item(selected_row, 0).text()
            current_path = self.table.item(selected_row, 1).text()
            selected_node = next((node for node in get_filecache_nodes() if node.name() == node_name), None)
            
            if selected_node:
                new_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", current_path)
                if new_path:
                    print(f"Editing path for node: {selected_node.name()}")
                    selected_node.parm("file").set(new_path)
                    self.table.item(selected_row, 1).setText(new_path)
                    self.adjust_sizes()


    def adjust_sizes(self):
        self.table.resizeColumnToContents(1)
        width = self.table.verticalHeader().width() + self.table.columnWidth(0) + self.table.columnWidth(1) + 50
        height = self.table.horizontalHeader().height() + (self.table.rowHeight(0) * self.table.rowCount()) + 50
        self.resize(width, height)

# Manually initiate the GUI
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
window = FileCacheNodeEditor()
window.show()
