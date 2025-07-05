import json
import os

class ProgressStorage:
    def __init__(self, storage_file="progress.json"):
        self.storage_file = storage_file
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, "w") as f:
                json.dump({}, f)

    def save_progress(self, player_id: int, progress: dict):
        with open(self.storage_file, "r+") as f:
            data = json.load(f)
            data[str(player_id)] = progress
            f.seek(0)
            json.dump(data, f, indent=4)

    def load_progress(self, player_id: int) -> dict:
        with open(self.storage_file, "r") as f:
            data = json.load(f)
            return data.get(str(player_id), {"levels_completed": [], "points": 0, "achievements": []})