import requests
import importlib.util
import sys
import tempfile

owner = "eotter-beep"
repo = "mixidevelopers"
package = input("Enter package name: ")
path_to_module = input("Path to open the Mix library (e.g., __main__.py): ")

# Fetch the file from GitHub API
url = f"https://api.github.com/repos/{owner}/{repo}/contents/packages/{package}/{path_to_module}"
response = requests.get(url)

if response.status_code == 200:
    import base64
    code = base64.b64decode(response.json()['content']).decode('utf-8')

    # Write code to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp_file:
        tmp_file.write(code.encode('utf-8'))
        tmp_path = tmp_file.name

    # Dynamically import the module
    spec = importlib.util.spec_from_file_location("mix_package", tmp_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mix_package"] = module
    spec.loader.exec_module(module)
    print(f"Package '{package}' loaded successfully.")
else:
    print(f"Failed to fetch package '{package}'. Status code: {response.status_code}")
