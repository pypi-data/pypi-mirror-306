"""Tool for the Loan API (get user's card details)."""

from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from wktools_langflow.wrapper.card_wrapper import CardWrapper


class CardQueryInput(BaseModel):
    """Input for the CardQueryInput tool."""

    user_id: str = Field(description="user's id", default="wk")
    card_last_4_digits: str = Field(description="user's card last 4 digits", default="0000")


class GetAllCardQueryRun(BaseTool):
    """Tool for the Card API (get user's all cards)."""
    name: str = "get_all_card_list"
    description: str = (
        "A wrapper for getting card list. "
        "Useful for when you need to answer questions about to get current user's all cards "
        "Get user's all cards. ")
    api_wrapper: CardWrapper

    args_schema: Type[BaseModel] = CardQueryInput

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        user_id: str = None,
    ) -> str:
        """Use the Card tool."""
        return self.api_wrapper.get_all_cards()


class GetCardByCardLast4DigitNumber(BaseTool):
    """Tool for the Card API (get user's card by card last 4-digit number)."""

    name: str = "get_card_by_card_last_4_digit_number"
    description: str = (
        "A wrapper for getting card details by providing card last 4 digits number. "
        "Useful for when you need to answer questions about to get current user's card by card last 4 digits number."
        "Get user's card detail by card last 4 digits number.")
    api_wrapper: CardWrapper

    args_schema: Type[BaseModel] = CardQueryInput

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        card_last_4_digits: str = None,
    ) -> str:
        """Use the Card tool."""
        return self.api_wrapper.get_card(card_last_4_digits)
