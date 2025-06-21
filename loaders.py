import json
import os


class JSONLoader:

    __folder_path: str = "JSONs"
    __booster_x2_file_name: str = "boosterX2.json"
    __score_file_name: str = "score.json"

    @staticmethod
    def load_score() -> dict[str, int | dict[str, int]]:

        file_path = os.path.join(JSONLoader.__folder_path, JSONLoader.__score_file_name)

        if not os.path.exists(JSONLoader.__folder_path):
            os.makedirs(JSONLoader.__folder_path)

        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump({"counter": 0}, file)
            return {"counter": 0}

        with open(file_path, "r") as file:
            text_json = file.read()
            if text_json != "":
                dictionary = json.loads(text_json)
            else:
                dictionary = {"counter": 0}

        return dictionary

    @staticmethod
    def load_booster_x2() -> list[int]:

        file_path = os.path.join(JSONLoader.__folder_path, JSONLoader.__booster_x2_file_name)

        if not os.path.exists(JSONLoader.__folder_path):
            os.makedirs(JSONLoader.__folder_path)

        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump([], file)
            return []

        with open(file_path, "r") as file:
            text_json = file.read()
            if text_json != "":
                dictionary = json.loads(text_json)
            else:
                dictionary = []

        return dictionary

    @staticmethod
    def update_score(dictionary: dict[str, int | dict[str, int]]) -> None:
        file_path = os.path.join(JSONLoader.__folder_path, JSONLoader.__score_file_name)
        with open(file_path, "w") as file:
            jason = json.dumps(dictionary)
            file.write(jason)

    @staticmethod
    def update_boost_list(boost_list: list[int]) -> None:
        file_path = os.path.join(JSONLoader.__folder_path, JSONLoader.__booster_x2_file_name)
        with open(file_path, "w") as file:
            jason = json.dumps(boost_list)
            file.write(jason)

    @staticmethod
    def get_boost_names(boost_list: list[int], score_dict: dict[str, int | dict[str, int]]) -> str:
        result: str = "\n\n<b>Список Boost X2:</b>\n\n"
        if len(boost_list) > 0:
            for x in boost_list:
                result += f"🔼{score_dict[str(x)]['name']}🔼\n"
        else:
            result = ""

        return result
