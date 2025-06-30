"""
VEX Code Snippet Manager

A utility for managing and organizing VEX code snippets with categories.
Allows users to store, organize, and quickly access VEX code snippets.

Author: BYVFX Tools
"""

import hou
import json
import os
from typing import Dict, List, Optional, Tuple
from PySide2 import QtWidgets, QtCore, QtGui

# Constants
HOUDINI_USER_PATH = hou.getenv("HOUDINI_USER_PREF_DIR")
VEX_SNIPPETS_FILE = os.path.join(HOUDINI_USER_PATH, "scripts", "vex_snippets.json")

class VEXSnippetManager:
    """Core class for managing VEX snippets data."""
    
    def __init__(self):
        self.snippets_data = {}
        self.categories = []
        self.load_snippets()
    
    def load_snippets(self) -> None:
        """Load snippets from JSON file."""
        try:
            if os.path.exists(VEX_SNIPPETS_FILE):
                with open(VEX_SNIPPETS_FILE, 'r') as file:
                    data = json.load(file)
                    self.snippets_data = data.get("snippets", {})
                    self.categories = data.get("categories", self._get_default_categories())
            else:
                self._create_default_data()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading VEX snippets: {e}")
            self._create_default_data()
    
    def save_snippets(self) -> None:
        """Save snippets to JSON file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(VEX_SNIPPETS_FILE), exist_ok=True)
            
            data = {
                "categories": self.categories,
                "snippets": self.snippets_data
            }
            
            with open(VEX_SNIPPETS_FILE, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving VEX snippets: {e}")
    
    def _get_default_categories(self) -> List[str]:
        """Get default VEX categories."""
        return [
            "Attributes",
            "Noise Functions", 
            "Math/Utility",
            "Geometry Processing",
            "Color/Shading",
            "Animation/Time",
            "Particles",
            "Volumes",
            "Custom",
            "Uncategorized"
        ]
    
    def _create_default_data(self) -> None:
        """Create default snippet data with examples."""
        self.categories = self._get_default_categories()
        self.snippets_data = {
            "Attributes": {
                "Random Color per Point": {
                    "code": '@Cd = rand(@ptnum);',
                    "description": "Assigns random color to each point",
                    "tags": ["color", "random", "point"]
                },
                "Scale by Point Number": {
                    "code": '@pscale = fit01(@ptnum/@numpt, 0.1, 1.0);',
                    "description": "Scale points based on point number",
                    "tags": ["scale", "point", "fit"]
                }
            },
            "Noise Functions": {
                "Turbulent Position": {
                    "code": 'vector turb = noise(@P * 5) * 0.1;\n@P += turb;',
                    "description": "Add turbulent noise to point positions",
                    "tags": ["noise", "position", "turbulence"]
                },
                "Animated Noise": {
                    "code": 'float n = noise(@P * 2 + @Time);\n@Cd = n;',
                    "description": "Time-based animated noise for color",
                    "tags": ["noise", "animation", "time", "color"]
                }
            },
            "Math/Utility": {
                "Distance from Origin": {
                    "code": 'float dist = length(@P);\n@dist = dist;',
                    "description": "Calculate distance from origin",
                    "tags": ["distance", "math", "utility"]
                },
                "Remap Values": {
                    "code": '@value = fit(@input, @old_min, @old_max, @new_min, @new_max);',
                    "description": "Remap values from one range to another",
                    "tags": ["remap", "fit", "utility"]
                }
            }
        }
        self.save_snippets()
    
    def add_snippet(self, category: str, name: str, code: str, 
                   description: str = "", tags: List[str] = None) -> bool:
        """Add a new snippet."""
        if tags is None:
            tags = []
        
        if category not in self.categories:
            self.categories.append(category)
        
        if category not in self.snippets_data:
            self.snippets_data[category] = {}
        
        self.snippets_data[category][name] = {
            "code": code,
            "description": description,
            "tags": tags
        }
        
        self.save_snippets()
        return True
    
    def delete_snippet(self, category: str, name: str) -> bool:
        """Delete a snippet."""
        try:
            if category in self.snippets_data and name in self.snippets_data[category]:
                del self.snippets_data[category][name]
                
                # Remove empty categories
                if not self.snippets_data[category]:
                    del self.snippets_data[category]
                
                self.save_snippets()
                return True
        except Exception as e:
            print(f"Error deleting snippet: {e}")
        return False
    
    def get_snippet(self, category: str, name: str) -> Optional[Dict]:
        """Get a specific snippet."""
        if category in self.snippets_data and name in self.snippets_data[category]:
            return self.snippets_data[category][name]
        return None
    
    def search_snippets(self, query: str) -> List[Tuple[str, str, Dict]]:
        """Search snippets by name, description, or tags."""
        results = []
        query_lower = query.lower()
        
        for category, snippets in self.snippets_data.items():
            for name, data in snippets.items():
                # Search in name
                if query_lower in name.lower():
                    results.append((category, name, data))
                    continue
                
                # Search in description
                if query_lower in data.get("description", "").lower():
                    results.append((category, name, data))
                    continue
                
                # Search in tags
                tags = data.get("tags", [])
                if any(query_lower in tag.lower() for tag in tags):
                    results.append((category, name, data))
        
        return results


class VEXSnippetManagerUI(QtWidgets.QDialog):
    """UI for the VEX Snippet Manager."""
    
    def __init__(self, parent=None):
        super(VEXSnippetManagerUI, self).__init__(parent)
        self.manager = VEXSnippetManager()
        self.setup_ui()
        self.populate_tree()
        
    def setup_ui(self) -> None:
        """Setup the user interface."""
        self.setWindowTitle("VEX Snippet Manager")
        self.setModal(False)
        self.resize(800, 600)
        
        # Main layout
        layout = QtWidgets.QVBoxLayout(self)
        
        # Search bar
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(QtWidgets.QLabel("Search:"))
        
        self.search_line = QtWidgets.QLineEdit()
        self.search_line.setPlaceholderText("Search snippets...")
        self.search_line.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_line)
        
        self.search_clear_btn = QtWidgets.QPushButton("Clear")
        self.search_clear_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(self.search_clear_btn)
        
        layout.addLayout(search_layout)
        
        # Main content area
        content_layout = QtWidgets.QHBoxLayout()
        
        # Left panel - snippet tree
        left_panel = QtWidgets.QVBoxLayout()
        
        # Tree widget
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabel("VEX Snippets")
        self.tree.itemClicked.connect(self.on_snippet_selected)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        left_panel.addWidget(self.tree)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        self.add_btn = QtWidgets.QPushButton("Add Snippet")
        self.add_btn.clicked.connect(self.add_snippet)
        button_layout.addWidget(self.add_btn)
        
        self.add_category_btn = QtWidgets.QPushButton("Add Category")
        self.add_category_btn.clicked.connect(self.add_category)
        button_layout.addWidget(self.add_category_btn)
        
        left_panel.addLayout(button_layout)
        
        # Right panel - snippet details
        right_panel = QtWidgets.QVBoxLayout()
        
        # Snippet info
        info_layout = QtWidgets.QFormLayout()
        
        self.snippet_name = QtWidgets.QLabel("Select a snippet")
        self.snippet_name.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addRow("Name:", self.snippet_name)
        
        self.snippet_description = QtWidgets.QLabel("")
        self.snippet_description.setWordWrap(True)
        info_layout.addRow("Description:", self.snippet_description)
        
        self.snippet_tags = QtWidgets.QLabel("")
        info_layout.addRow("Tags:", self.snippet_tags)
        
        right_panel.addLayout(info_layout)
        
        # Code editor
        right_panel.addWidget(QtWidgets.QLabel("VEX Code:"))
        self.code_editor = QtWidgets.QTextEdit()
        self.code_editor.setFont(QtGui.QFont("Courier", 10))
        self.code_editor.setReadOnly(True)
        right_panel.addWidget(self.code_editor)
        
        # Action buttons
        action_layout = QtWidgets.QHBoxLayout()
        
        self.copy_btn = QtWidgets.QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setEnabled(False)
        action_layout.addWidget(self.copy_btn)
        
        self.edit_btn = QtWidgets.QPushButton("Edit Snippet")
        self.edit_btn.clicked.connect(self.edit_snippet)
        self.edit_btn.setEnabled(False)
        action_layout.addWidget(self.edit_btn)
        
        right_panel.addLayout(action_layout)
        
        # Add panels to content layout
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setMaximumWidth(300)
        
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(right_panel)
        
        content_layout.addWidget(left_widget)
        content_layout.addWidget(right_widget)
        
        layout.addLayout(content_layout)
        
        # Status bar
        self.status_label = QtWidgets.QLabel("Ready")
        layout.addWidget(self.status_label)
    
    def populate_tree(self) -> None:
        """Populate the tree widget with snippets."""
        self.tree.clear()
        
        for category in self.manager.categories:
            if category in self.manager.snippets_data:
                snippets = self.manager.snippets_data[category]
                if snippets:  # Only show categories that have snippets
                    category_item = QtWidgets.QTreeWidgetItem(self.tree, [category])
                    category_item.setData(0, QtCore.Qt.UserRole, ("category", category))
                    
                    for snippet_name in sorted(snippets.keys()):
                        snippet_item = QtWidgets.QTreeWidgetItem(category_item, [snippet_name])
                        snippet_item.setData(0, QtCore.Qt.UserRole, ("snippet", category, snippet_name))
        
        self.tree.expandAll()
    
    def on_snippet_selected(self, item: QtWidgets.QTreeWidgetItem, column: int) -> None:
        """Handle snippet selection."""
        data = item.data(0, QtCore.Qt.UserRole)
        
        if data and data[0] == "snippet":
            _, category, name = data
            snippet = self.manager.get_snippet(category, name)
            
            if snippet:
                self.snippet_name.setText(name)
                self.snippet_description.setText(snippet.get("description", "No description"))
                self.snippet_tags.setText(", ".join(snippet.get("tags", [])))
                self.code_editor.setPlainText(snippet.get("code", ""))
                
                self.copy_btn.setEnabled(True)
                self.edit_btn.setEnabled(True)
                
                self.current_category = category
                self.current_snippet = name
        else:
            self.clear_selection()
    
    def clear_selection(self) -> None:
        """Clear the current selection."""
        self.snippet_name.setText("Select a snippet")
        self.snippet_description.setText("")
        self.snippet_tags.setText("")
        self.code_editor.setPlainText("")
        self.copy_btn.setEnabled(False)
        self.edit_btn.setEnabled(False)
        self.current_category = None
        self.current_snippet = None
    
    def copy_to_clipboard(self) -> None:
        """Copy the current snippet code to clipboard."""
        code = self.code_editor.toPlainText()
        if code:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(code)
            self.status_label.setText("Code copied to clipboard!")
            QtCore.QTimer.singleShot(2000, lambda: self.status_label.setText("Ready"))
    
    def on_search(self, text: str) -> None:
        """Handle search input."""
        if not text.strip():
            self.populate_tree()
            return
        
        self.tree.clear()
        results = self.manager.search_snippets(text)
        
        if results:
            # Group results by category
            categories = {}
            for category, name, data in results:
                if category not in categories:
                    categories[category] = []
                categories[category].append((name, data))
            
            for category, snippets in categories.items():
                category_item = QtWidgets.QTreeWidgetItem(self.tree, [f"{category} (Search Results)"])
                category_item.setData(0, QtCore.Qt.UserRole, ("category", category))
                
                for name, data in snippets:
                    snippet_item = QtWidgets.QTreeWidgetItem(category_item, [name])
                    snippet_item.setData(0, QtCore.Qt.UserRole, ("snippet", category, name))
            
            self.tree.expandAll()
        else:
            QtWidgets.QTreeWidgetItem(self.tree, ["No results found"])
    
    def clear_search(self) -> None:
        """Clear the search and repopulate tree."""
        self.search_line.clear()
        self.populate_tree()
    
    def add_snippet(self) -> None:
        """Add a new snippet."""
        dialog = VEXSnippetDialog(self.manager.categories, parent=self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            snippet_data = dialog.get_snippet_data()
            
            success = self.manager.add_snippet(
                snippet_data["category"],
                snippet_data["name"],
                snippet_data["code"],
                snippet_data["description"],
                snippet_data["tags"]
            )
            
            if success:
                self.populate_tree()
                self.status_label.setText("Snippet added successfully!")
                QtCore.QTimer.singleShot(2000, lambda: self.status_label.setText("Ready"))
    
    def add_category(self) -> None:
        """Add a new category."""
        text, ok = QtWidgets.QInputDialog.getText(
            self, "Add Category", "Category name:"
        )
        
        if ok and text.strip():
            if text not in self.manager.categories:
                self.manager.categories.append(text)
                self.manager.save_snippets()
                self.status_label.setText(f"Category '{text}' added!")
                QtCore.QTimer.singleShot(2000, lambda: self.status_label.setText("Ready"))
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Warning", f"Category '{text}' already exists!"
                )
    
    def edit_snippet(self) -> None:
        """Edit the current snippet."""
        if hasattr(self, 'current_category') and hasattr(self, 'current_snippet'):
            snippet = self.manager.get_snippet(self.current_category, self.current_snippet)
            if snippet:
                dialog = VEXSnippetDialog(
                    self.manager.categories,
                    edit_mode=True,
                    category=self.current_category,
                    name=self.current_snippet,
                    code=snippet["code"],
                    description=snippet.get("description", ""),
                    tags=snippet.get("tags", []),
                    parent=self
                )
                
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    # Delete old snippet
                    self.manager.delete_snippet(self.current_category, self.current_snippet)
                    
                    # Add updated snippet
                    snippet_data = dialog.get_snippet_data()
                    self.manager.add_snippet(
                        snippet_data["category"],
                        snippet_data["name"],
                        snippet_data["code"],
                        snippet_data["description"],
                        snippet_data["tags"]
                    )
                    
                    self.populate_tree()
                    self.clear_selection()
                    self.status_label.setText("Snippet updated successfully!")
                    QtCore.QTimer.singleShot(2000, lambda: self.status_label.setText("Ready"))
    
    def show_context_menu(self, position: QtCore.QPoint) -> None:
        """Show context menu for tree items."""
        item = self.tree.itemAt(position)
        if not item:
            return
        
        data = item.data(0, QtCore.Qt.UserRole)
        if not data:
            return
        
        menu = QtWidgets.QMenu(self)
        
        if data[0] == "snippet":
            _, category, name = data
            
            edit_action = menu.addAction("Edit Snippet")
            edit_action.triggered.connect(self.edit_snippet)
            
            delete_action = menu.addAction("Delete Snippet")
            delete_action.triggered.connect(lambda: self.delete_snippet(category, name))
            
            menu.addSeparator()
            copy_action = menu.addAction("Copy Code")
            copy_action.triggered.connect(self.copy_to_clipboard)
        
        menu.exec_(self.tree.mapToGlobal(position))
    
    def delete_snippet(self, category: str, name: str) -> None:
        """Delete a snippet with confirmation."""
        reply = QtWidgets.QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete the snippet '{name}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            if self.manager.delete_snippet(category, name):
                self.populate_tree()
                self.clear_selection()
                self.status_label.setText("Snippet deleted successfully!")
                QtCore.QTimer.singleShot(2000, lambda: self.status_label.setText("Ready"))


class VEXSnippetDialog(QtWidgets.QDialog):
    """Dialog for adding/editing VEX snippets."""
    
    def __init__(self, categories: List[str], edit_mode: bool = False,
                 category: str = "", name: str = "", code: str = "",
                 description: str = "", tags: List[str] = None, parent=None):
        super(VEXSnippetDialog, self).__init__(parent)
        self.categories = categories
        self.edit_mode = edit_mode
        
        if tags is None:
            tags = []
        
        self.setup_ui()
        
        # Populate fields if editing
        if edit_mode:
            self.category_combo.setCurrentText(category)
            self.name_edit.setText(name)
            self.code_edit.setPlainText(code)
            self.description_edit.setText(description)
            self.tags_edit.setText(", ".join(tags))
    
    def setup_ui(self) -> None:
        """Setup the dialog UI."""
        title = "Edit Snippet" if self.edit_mode else "Add New Snippet"
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # Form layout
        form_layout = QtWidgets.QFormLayout()
        
        # Category
        self.category_combo = QtWidgets.QComboBox()
        self.category_combo.addItems(self.categories)
        self.category_combo.setEditable(True)
        form_layout.addRow("Category:", self.category_combo)
        
        # Name
        self.name_edit = QtWidgets.QLineEdit()
        form_layout.addRow("Name:", self.name_edit)
        
        # Description
        self.description_edit = QtWidgets.QLineEdit()
        form_layout.addRow("Description:", self.description_edit)
        
        # Tags
        self.tags_edit = QtWidgets.QLineEdit()
        self.tags_edit.setPlaceholderText("Comma-separated tags")
        form_layout.addRow("Tags:", self.tags_edit)
        
        layout.addLayout(form_layout)
        
        # Code editor
        layout.addWidget(QtWidgets.QLabel("VEX Code:"))
        self.code_edit = QtWidgets.QTextEdit()
        self.code_edit.setFont(QtGui.QFont("Courier", 10))
        layout.addWidget(self.code_edit)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        self.ok_btn = QtWidgets.QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def get_snippet_data(self) -> Dict:
        """Get the snippet data from the form."""
        tags_text = self.tags_edit.text().strip()
        tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()] if tags_text else []
        
        return {
            "category": self.category_combo.currentText().strip(),
            "name": self.name_edit.text().strip(),
            "code": self.code_edit.toPlainText(),
            "description": self.description_edit.text().strip(),
            "tags": tags
        }
    
    def accept(self) -> None:
        """Validate and accept the dialog."""
        data = self.get_snippet_data()
        
        if not data["category"]:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a category!")
            return
        
        if not data["name"]:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a name!")
            return
        
        if not data["code"]:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter VEX code!")
            return
        
        super(VEXSnippetDialog, self).accept()


def show_vex_snippet_manager():
    """Show the VEX Snippet Manager UI."""
    global vex_snippet_ui
    
    try:
        vex_snippet_ui.close()
    except (NameError, AttributeError):
        pass
    
    vex_snippet_ui = VEXSnippetManagerUI(hou.qt.mainWindow())
    vex_snippet_ui.show()


# Convenience functions for quick access
def get_vex_manager() -> VEXSnippetManager:
    """Get a VEX snippet manager instance."""
    return VEXSnippetManager()


def quick_add_snippet(category: str, name: str, code: str, 
                     description: str = "", tags: List[str] = None) -> bool:
    """Quick function to add a snippet programmatically."""
    manager = VEXSnippetManager()
    return manager.add_snippet(category, name, code, description, tags)


if __name__ == "__main__":
    show_vex_snippet_manager()
