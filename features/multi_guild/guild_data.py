import json

class GuildData():
    # コンストラクタ
    def __init__(self, guild_id, ch_id, user_id, h1 = 7, m1 = 0, h2 = 21, m2 = 0):
        self.guild_id: int = int(guild_id)
        self.ch_id: int = int(ch_id)
        self.user_id = int(user_id)
        self.h1: int = int(h1)
        self.m1: int = int(m1)
        self.h2: int = int(h2)
        self.m2: int = int(m2)

    
    # 適切な辞書型からインスタンスを作成
    @classmethod
    def import_from_dict(cls, data: dict) -> "GuildData":
        try:
            return cls(guild_id = data["guild_id"], ch_id = data["ch_id"], user_id = data["user_id"], h1 = data["h1"], m1 = data["m1"], h2 = data["h2"], m2 = data["m2"])
        except KeyError as e:
            raise

    # 情報を辞書型にエクスポート
    def export_to_dict(self) -> dict:
        return_dict = {"guild_id": self.guild_id, "ch_id": self.ch_id, "user": self.user_id, "h1": self.h1, "m1": self.m1, "h2": self.h2, "m2": self.m2}
        return return_dict