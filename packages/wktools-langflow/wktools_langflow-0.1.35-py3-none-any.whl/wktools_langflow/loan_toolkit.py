"""Tool for the Loan API (get user's loan profiles)."""

from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from wktools_langflow.wrapper.loan_wrapper import LoanWrapper


class LoanQueryInput(BaseModel):
    """Input for the LoanQueryInput tool."""

    user_id: str = Field(description="user's id", default="wk")
    loan_account_number: str = Field(description="user's loan account number", default="111222333")

class UpdateOutstandingRequest(BaseModel):
    loan_account_number: str
    pay_amount: float

# class LoanQueryRun(BaseTool):
#     """Tool for the Loan API (get user's loan profiles)."""
#
#     name: str = "loan"
#     description: str = (
#         "A wrapper for loan. "
#         "Useful for when you need to answer questions about to get  current user's all loan profiles "
#         "Get user's all loan profiles.")
#     api_wrapper: LoanWrapper
#
#     args_schema: Type[BaseModel] = LoanQueryInput
#
#     def _run(
#         self,
#         run_manager: Optional[CallbackManagerForToolRun] = None,
#     ) -> str:
#         """Use the Loan tool."""
#         return self.api_wrapper.get_user_loan_profiles()

class LoanQueryRun(BaseTool):
    """Tool for the Loan API (get user's loan profiles)."""
    name: str = "get_user_loan_profile_list"
    description: str = (
        "A wrapper for getting loan profile list. "
        "Useful for when you need to answer questions about to get  current user's all loan profiles "
        "Get user's all loan profiles.")
    api_wrapper: LoanWrapper

    args_schema: Type[BaseModel] = LoanQueryInput

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        user_id: str = None,
    ) -> str:
        """Use the Loan tool."""
        # self.user_id = self.api_wrapper.user_id
        return self.api_wrapper.get_user_loan_profiles()

    # get_user_loan_profile_by_loan_account_number
class GetUserLoanProfileByLoanAccountNumber(BaseTool):
    """Tool for the Loan API (get user's loan profiles by loan account number)."""

    name: str = "get_user_loan_profile_by_loan_account_number"
    description: str = (
        "A wrapper for getting loan profile by providing loan account number. "
        "Useful for when you need to answer questions about to get current user's loans by loan account number."
        "Get user's loan profiles by loan account number.")
    api_wrapper: LoanWrapper

    args_schema: Type[BaseModel] = LoanQueryInput

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the Loan tool."""
        # self.loan_account_number = self.api_wrapper.loan_account_number
        return self.api_wrapper.get_user_loan_profile_by_loan_account_number(self.loan_account_number)

#     update_outstanding
class UpdateLoanOutStandingBalancdeQueryRun(BaseTool):
    """Tool for the Loan API (update user's loan outstanding amount)."""

    name: str = "loan"
    description: str = (
        "A wrapper for loan. "
        "Useful for when you need to answer questions about current user's loans. "
        "Update user's loan outstanding amount by loan account when user pays.")
    api_wrapper: LoanWrapper

    args_schema: Type[BaseModel] = UpdateOutstandingRequest

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Loan tool."""
        return self.api_wrapper.get_user_loan_profiles(UpdateOutstandingRequest(loan_account_number=self.args_schema.loan_account_number, pay_amount=self.args_schema.pay_amount))
