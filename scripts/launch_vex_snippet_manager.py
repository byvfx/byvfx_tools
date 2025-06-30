"""
VEX Snippet Manager Launcher Script

This script can be used in Houdini shelf tools or menu items to launch
the VEX Snippet Manager.
"""

try:
    from byvfx.utils.vex_snippet_manager import show_vex_snippet_manager
    show_vex_snippet_manager()
except ImportError as e:
    import hou
    hou.ui.displayMessage(
        f"Could not import VEX Snippet Manager: {e}\n\n"
        "Please ensure the byvfx_tools package is properly installed.",
        severity=hou.severityType.Error,
        title="VEX Snippet Manager"
    )
except Exception as e:
    import hou
    hou.ui.displayMessage(
        f"Error launching VEX Snippet Manager: {e}",
        severity=hou.severityType.Error,
        title="VEX Snippet Manager"
    )
