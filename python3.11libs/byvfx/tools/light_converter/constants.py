from typing import Dict, Any

SUPPORTED_LIGHTS = {
    # Mantra lights
    "hlight": "Mantra",
    "envlight": "Mantra",
    # Redshift lights
    "rslight": "Redshift",
    "rslightdome": "Redshift",
    #Octane lights
    "octane_light": "Octane"
}

MANTRA_TO_REDSHIFT_PARAMS: Dict[str, str] = {
    "light_intensity": "RSL_intensityMultiplier",
    "light_exposure": "Light1_exposure",
    "env_map": "env_map",
    "light_color": "lightcolor",
    "light_colorr": "light_colorr",
    "light_colorg": "light_colorg",
    "light_colorb": "light_colorb",
    "light_type": "light_type",
    "coneangle": "coneangle",
    "areageometry": "RSL_meshObject",
}

REDSHIFT_TO_MANTRA_PARAMS: Dict[str, str] = {
    "RSL_intensityMultiplier": "light_intensity",
    "Light1_exposure": "light_exposure",
    "env_map": "env_map",
    "lightcolor": "light_color",
    "light_colorr": "light_colorr",
    "light_colorg": "light_colorg",
    "light_colorb": "light_colorb",
    "light_type": "light_type",
    "coneangle": "coneangle",
}

OCTANE_TO_MANTRA_PARAMS: Dict[str, str] = {
    
    "NT_MAT_DIFFUSE1_diffuse": "light_color",
}
    

MANTRA_TO_REDSHIFT_MODES: Dict[int, int] = {
    0: 1,  # Directional
    1: 3,  # Area
    2: 3,  # Area
    3: 3,  # Area
    4: 3,  # Area
    5: 3,  # Area
    6: 3,  # Area
    7: 3,  # Area
    8: 0,  # Point
}

REDSHIFT_TO_MANTRA_MODES: Dict[int, int] = {
    0: 7,  # Point light
    1: 0,  # Directional light
    2: 0,  # Spot light
    3: 2,  # Area light
}

LIGHT_TYPE_MAPPING = {
    # Mantra to Redshift
    "hlight": "rslight",
    "envlight": "rslightdome",
    # Redshift to Mantra
    "rslight": "hlight",
    "rslightdome": "envlight"
}
