from typing import Dict

from langchain_core.utils import get_from_dict_or_env
from pydantic.v1 import root_validator, BaseModel
import requests
import json


class CardWrapper(BaseModel):
    openai_api_key: str
    card_last_4_digits: str = None
    user_id: str = None

    class Config:
        extra = "forbid"

    # noinspection PyMethodParameters
    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and endpoint exists in environment."""
        openai_api_key = get_from_dict_or_env(
            values, "openai_api_key", "OPENAI_API_KEY"
        )
        values["openai_api_key"] = openai_api_key

        return values


    def get_all_cards(self):
        url = f"http://localhost:8000/api/cards/user/{self.user_id}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print(response.json())

            limited_results = []
            for result in json.loads(response.content):
                limited_result = {
                "snippet": result,
                }
                limited_results.append(limited_result)

            return limited_results
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    # user/{user_name}/card/{card_last_4_digits}
    def get_card(self, card_last_4_digits):
        url = f"http://localhost:8000/api/cards/{self.user_id}/card/{card_last_4_digits}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print(response.json())

            limited_results = []
            limited_result = {
            "snippet": response.content,
            }
            limited_results.append(limited_result)

            return limited_results
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
