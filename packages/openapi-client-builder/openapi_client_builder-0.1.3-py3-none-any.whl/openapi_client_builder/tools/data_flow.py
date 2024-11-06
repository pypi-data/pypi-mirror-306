import os
import json
import requests


def get_openapi_json(url_or_path: str) -> dict | None:
    """
    Fetches and returns OpenAPI JSON data.

    Args:
        url_or_path (str): The URL to fetch the OpenAPI JSON data from.

    Returns:
        dict | None: The OpenAPI JSON data if retrieval is successful,
                     otherwise None.
    """
    try:
        response = requests.get(url_or_path)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(
                "Failed to retrieve data. Status code:",
                response.status_code,
            )
    except requests.RequestException as e:
        print("Error during request:\n", e)


def output_file(
    name: str, data: str | dict, output_dir: str = "./dist"
) -> None:  # noqa
    """
    Writes data to a file in the specified output directory.

    Args:
        name (str): The name of the output file.
        data (str | dict): The data to be written to the file.
                           If data is a dict, it will be JSON serialized.
        output_dir (str, optional): The output directory where
                                    the file will be created.
                                    Defaults to "./dist/".
                           €
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if isinstance(data, dict):
        data = json.dumps(data, indent=4, ensure_ascii=False)

    with open(f"{output_dir}/{name}", "w", encoding="utf-8") as f:
        f.write(data)
