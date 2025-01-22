import hou
import re

def get_all_parms(kwargs, unlocked_only=False):
    """
    Get all (both normal and locked) parms, related to an RMB menu click.
    
    Args:
        kwargs (dict): Dictionary containing keyword arguments
        unlocked_only (bool): Whether to include only unlocked parameters
        
    Returns:
        list: List of parameters
    """
    r = None
    try:
        r = kwargs["parms"]
        if not unlocked_only:
            r += kwargs["locked_parms"]
    except:
        pass
    return r

def reset_parms(kwargs, unlocked_only=False):
    """
    Reset all parameters to their default state.
    Especially important is to remove all expression links, as they can
    throw off setting values (the values will be set on parms pointed to
    by the expression). 

    Hopefully this covers all (or, most) scenarios.
    
    Args:
        kwargs (dict): Dictionary containing keyword arguments
        unlocked_only (bool): Whether to include only unlocked parameters
    """
    try:
        parms = get_all_parms(kwargs, unlocked_only=unlocked_only)
        for parm in parms:
            parm.lock(False)
            parm.deleteAllKeyframes()
            parm.revertToDefaults()
    except:
        pass
    
def reset_parm(parm):
    """
    Reset a single parameter to its default state.
    
    Args:
        parm (hou.Parm): The parameter to reset
    """
    reset_parms({"parms": (parm,)})

def toggle_abs_rel_path(kwargs):
    """
    Converts between absolute and relative OP paths.
    (Called from PARMmenu.xml)
    
    Args:
        kwargs (dict): Dictionary containing keyword arguments
    """
    parms = get_all_parms(kwargs)
    to_abs = None  # None=yet to be decided, True=convert to abs 1=to rel

    for parm in parms:
        pnode = parm.node()
        paths_in = parm.evalAsString().split()  # paths as string
        paths_out = []

        for path in paths_in:
            parmname = ""
            if pnode.parm(path):
                # if it's a parm, pop/remember parm name and still deal w/ node paths
                parmname = re.search("/[^/]+$", path).group(0)
                path = re.sub(parmname + "$", "", path)

            target = pnode.node(path)

            if target:
                # works with single nodes but not with patterns
                path_rel = pnode.relativePathTo(target)
                path_abs = target.path()

                # decide if we want to convert all to abs or rel
                if to_abs is None:
                    to_abs = re.sub("[/]+$", "", path) != path_abs  # (strip trailing slashes for comparison)

                paths_out.append((path_abs if to_abs else path_rel) + parmname)
            else:
                # probably a pattern, don't deal with it
                paths_out.append(path + parmname)

        path = " ".join(paths_out)
        reset_parm(parm)
        parm.set(path)