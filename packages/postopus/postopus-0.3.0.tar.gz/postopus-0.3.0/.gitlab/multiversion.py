import json
from pathlib import Path

# artifacts for old versions are in postopus/docs/_build/html
# artifacts for the current main are in docs/_build_html
old_versions = list(Path("postopus/docs/_build/html").glob("*"))

base_url = "https://octopus-code.gitlab.io/postopus/"

versions = [{"version": "dev", "url": base_url}]
for version in old_versions:
    versions.append({"version": version.name, "url": f"{base_url}{version.name}/"})

with open("docs/_build/html/_static/versions.json", "w") as f:
    json.dump(versions, f)
