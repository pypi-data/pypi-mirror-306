from postopus.namespace_utils import build_namespaces


def test_build_namespaces():
    expected_namespaces = [
        "Galaxy",
        "SolarSystem",
        "Galaxy.SolarSystem",
        "Earth",
        "Galaxy.SolarSystem.Earth",
    ]
    nspaces = build_namespaces("Galaxy.SolarSystem.Earth")
    assert nspaces == expected_namespaces
