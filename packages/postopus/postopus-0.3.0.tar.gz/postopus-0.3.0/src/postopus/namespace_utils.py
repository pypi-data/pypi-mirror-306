def build_namespaces(systemname: str):
    """
    Build all the possible namespaces, given a system name

    The prefixes of the parser.log variables associated with nested multisystems can
    be constructed in many different ways (namespaces). The namespaces always retain
    a hierarchical structure.

    E.g. if we have the system Galaxy.SolarSystem.Earth and we look for
    the associated TDTimeStep, we should look for:
    Galaxy.SolarSystem.Earth.TDTimeStep, Earth.TDTimeStep,
    Galaxy.SolarSystem.TDTimeStep, SolarSystem.TDTimeStep,
    Galaxy.TDTimeStep or just TDTimeStep (in this order!)

    When doing the search in the parser log we will do a reverse search, i.e. we
    will start from the last element and go upwards.

    We wouldn't find Earth.SolarSystem.TDTimeStep for instance, because this would
    break the hierarchy. Nor would we find SolarSystem.Earth, since the object of
    higher order 'Galaxy' would be missing.

    Parameters
    ----------
    systemname: str
        Full systemname.

    Returns
    -------
    All the possible namespaces for a given full system name.

    Example
    -------
    >>> build_namespaces('Galaxy.SolarSystem.Earth')
    ['Galaxy', 'SolarSystem', 'Galaxy.SolarSystem',
    'Earth', 'Galaxy.SolarSystem.Earth']



    """
    indiv_systems = systemname.split(".")  # [Galaxy, SolarSystem, Earth]
    full_hierarchy_paths = [
        ".".join(systemname.split(".")[:level])
        for level in range(2, len(indiv_systems) + 1)
    ]  # ['Galaxy.SolarSystem', 'Galaxy.SolarSystem.Earth']
    # initialize list, ignore first individual system at first, since indiv.
    # system list is longer by one element
    possible_namespaces = [None] * (
        len(indiv_systems) - 1 + len(full_hierarchy_paths)
    )  # 4

    possible_namespaces[0::2] = indiv_systems[1:]
    possible_namespaces[1::2] = full_hierarchy_paths

    possible_namespaces.insert(0, indiv_systems[0])  # Add the 5th one
    return possible_namespaces
