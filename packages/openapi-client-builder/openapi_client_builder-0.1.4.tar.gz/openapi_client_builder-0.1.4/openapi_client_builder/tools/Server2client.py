from .template import temp_header, temp_api


def get_api_path(api_path: str) -> str:
    """
    Convert an API path to a string with dynamic parts.

    This function takes an API path string and
    converts it to a string that includes dynamic parts.

    Args:
        api_path (str): The API path string that may contain dynamic parts enclosed in curly braces.

    Returns:
        str: The converted API path string with dynamic parts appropriately formatted.
    """
    path_parts: list = ["'"]
    path_list: list = api_path.split("/")[1:]
    path_list_len: int = len(path_list)
    for index, path_item in enumerate(path_list):
        if path_item.startswith("{") and path_item.endswith("}"):
            path_item = f"' + {path_item[1:-1]}" + (
                " + '" if index + 1 < path_list_len else ""
            )
            path_parts.append(path_item)
        else:
            path_parts.append(
                path_item if index + 1 < path_list_len else path_item + "'"
            )
    return "/".join(path_parts)


def get_api_parameters(parameters):
    """
    Generate a string representation of API parameters.

    This function takes a list of API parameters and
    creates a string representation of the parameters.

    Args:
        parameters (list): A list of dictionaries representing API parameters.

    Returns:
        str: representation of API parameters with name and type information.
    """
    return (
        (
            ",".join(
                [
                    f'{parameter["name"]} : {parameter["schema"]["type"]}'
                    for parameter in parameters
                ]
            )
        )
        .replace("array", "[]")
        .replace("integer", "number")
    )


def server2client(data_paths: dict) -> str:
    """
    Convert server data paths to client API functions.

    Args:
        data_paths (dict): A dictionary containing server data paths and associated information.

    Returns:
        str: A string representation of client API functions based on the input data paths.
    """
    api = ""
    for api_path, information in data_paths.items():
        # path name & parameters
        api_path = get_api_path(api_path)

        # mathod & all data
        for method, api_data in information.items():
            # fucntion name (use summary)
            summary: str = api_data["summary"]
            api_name_lists: list[str] = summary.split()
            api_name = api_name_lists[0].lower() + "".join(
                [name.capitalize() for name in api_name_lists[1:]]
            )
            # request body & parameters & path name (fucntion input...)
            api_body = ""
            api_parameters = (
                get_api_parameters(api_data["parameters"])
                if api_data.get("parameters")
                else ""
            )
            if api_data.get("requestBody"):
                api_schemas = api_data["requestBody"]["content"]
                if (api_schemas.get("application/json")):
                    api_schemas = api_schemas["application/json"]["schema"]["$ref"].split("/")[-1]
                elif (api_schemas.get("multipart/form-data")):
                    api_schemas = api_schemas["multipart/form-data"]["schema"]["properties"]
                    if (api_schemas.get("files")):
                        api_schemas = api_schemas.get("files")
                    elif (api_schemas.get("file")):
                        api_schemas = api_schemas.get("file")
                api_body = (
                    "\n\t\tbody: JSON.stringify(data)" if len(api_schemas) != 0 else ""
                )
                api_parameters = (" ," if len(api_parameters) else "") + api_parameters
                api_name += f"(data: {api_schemas} {api_parameters})"
            else:
                api_name += f"({api_parameters})"

            # responses type
            if api_data["responses"]["200"].get("content"):
                schema = api_data["responses"]["200"]["content"]["application/json"]["schema"]
                api_responses = (
                    schema["$ref"].split("/")[-1] if schema.get("$ref") else ""
                )
                # for typescript
                api_name += (
                    f": Promise<{api_responses}>" if len(api_responses) > 0 else ""
                )
            # download file use apiFile fucntion (use path name to check)
            api += temp_api % (
                api_name,
                api_path,
                method.upper(),
                api_body,
                "api" if "download" not in api_name else "apiFile",
            )
    return temp_header + api
