def read_api_key(api_key_path):
    with open(api_key_path, mode="r") as f:
        api_key = f.read().strip()
    return api_key
