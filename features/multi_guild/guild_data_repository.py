import json

from features.multi_guild import guild_data


class GuildDataRepository():
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_data(self) -> list:
        return_data = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                tmp = guild_data.GuildData.import_from_dict(i)
                return_data.append(tmp)
        return return_data