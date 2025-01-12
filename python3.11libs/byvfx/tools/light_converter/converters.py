import hou
from typing import List, Optional, Callable
from .constants import (
    MANTRA_TO_REDSHIFT_PARAMS, REDSHIFT_TO_MANTRA_PARAMS,
    MANTRA_TO_REDSHIFT_MODES, REDSHIFT_TO_MANTRA_MODES,
    LIGHT_TYPE_MAPPING
)

def _convert_light_node(
    node: hou.Node,
    param_mapping: dict,
    mode_mapping: dict,
    get_target_type: Callable[[str], str]
) -> Optional[hou.Node]:
    """Generic light conversion function"""
    main_node_type = node.type().name().split("::")[0]
    target_type = get_target_type(main_node_type)
    
    if not target_type:
        return None
        
    # Create new light
    parent = node.parent()
    new_node = parent.createNode(
        target_type,
        node_name=f"CONVERTED_{node.name()}"
    )
    
    # Copy parameters
    for source_param, target_param in param_mapping.items():
        if node.parm(source_param) and new_node.parm(target_param):
            if source_param == "light_type":
                _handle_light_type_conversion(
                    node, new_node, source_param, target_param, mode_mapping
                )
            else:
                new_node.parm(target_param).set(
                    node.parm(source_param).eval()
                )
    
    # Copy transform
    new_node.setWorldTransform(node.worldTransform())
    new_node.setPosition(node.position() + hou.Vector2(1, 0))
    
    return new_node

def _handle_light_type_conversion(
    source_node: hou.Node,
    target_node: hou.Node,
    source_param: str,
    target_param: str,
    mode_mapping: dict
) -> None:
    """Handle special case of light type conversion"""
    source_value = source_node.parm(source_param).eval()
    target_value = mode_mapping.get(source_value)
    
    if target_value is not None:
        target_node.parm(target_param).set(target_value)
        
        # Handle special cases (cone angle, area shape, etc.)
        if source_value == 2:  # Spotlight
            if target_node.parm("coneangle"):
                target_node.parm("coneangle").set(
                    source_node.parm("coneangle").eval()
                )
            if target_node.parm("coneenable"):
                target_node.parm("coneenable").set(1)

def convert_mantra_to_redshift(nodes: List[hou.Node]) -> List[hou.Node]:
    """Convert Mantra lights to Redshift"""
    if not nodes:
        raise ValueError("No nodes provided for conversion")
        
    converted = []
    for node in nodes:
        try:
            new_node = _convert_light_node(
                node,
                MANTRA_TO_REDSHIFT_PARAMS,
                MANTRA_TO_REDSHIFT_MODES,
                lambda t: LIGHT_TYPE_MAPPING.get(t)
            )
            if new_node:
                converted.append(new_node)
        except Exception as e:
            print(f"Error converting {node.path()}: {str(e)}")
            
    return converted

def convert_redshift_to_mantra(nodes: List[hou.Node]) -> List[hou.Node]:
    """Convert Redshift lights to Mantra"""
    if not nodes:
        raise ValueError("No nodes provided for conversion")
        
    converted = []
    for node in nodes:
        try:
            new_node = _convert_light_node(
                node,
                REDSHIFT_TO_MANTRA_PARAMS,
                REDSHIFT_TO_MANTRA_MODES,
                lambda t: LIGHT_TYPE_MAPPING.get(t)
            )
            if new_node:
                converted.append(new_node)
        except Exception as e:
            print(f"Error converting {node.path()}: {str(e)}")
            
    return converted