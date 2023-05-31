import json


class FileSystemService:
    def write_data_to_file(self, data, path):
        # Serializing json
        json_object = data.json()
        with open(path, "w") as output_file:
            output_file.write(json_object)

    def read_data_from_file(self, file_path):
        with open(file_path) as file_content:
            json_parsed_content = json.load(file_content)
        return json_parsed_content
