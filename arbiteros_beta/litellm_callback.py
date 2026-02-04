from typing import Any, Optional, Union

from litellm.caching.dual_cache import DualCache
from litellm.integrations.custom_logger import CustomLogger, UserAPIKeyAuth
from litellm.types.utils import CallTypesLiteral, LLMResponseTypes
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty

_console = Console()


# This file includes the custom callbacks for LiteLLM Proxy
# Once defined, these can be passed in proxy_config.yaml
class MyCustomHandler(CustomLogger):
    #### CALL HOOKS - proxy only ####
    """
    Control the modify incoming / outgoung data before calling the model
    """

    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: "DualCache",
        data: dict,
        call_type: CallTypesLiteral,
    ) -> Optional[
        Union[Exception, str, dict]
    ]:  # raise exception if invalid, return a str for the user to receive - if rejected, or return a modified dictionary for passing into litellm
        filtered_data = {
            k: data[k] for k in ["model", "messages", "tools"] if k in data
        }
        _console.print(
            Panel(
                Pretty(filtered_data),
                title="Pre Call Hook - Incoming Data",
            )
        )

    async def async_post_call_failure_hook(
        self,
        request_data: dict,
        original_exception: Exception,
        user_api_key_dict: UserAPIKeyAuth,
        traceback_str: Optional[str] = None,
    ) -> Any:
        _console.print(
            Panel(
                Pretty(original_exception),
                title="Post Call Failure Hook - Original Exception",
            )
        )
        _console.print(
            Panel(
                Pretty(traceback_str),
                title="Post Call Failure Hook - Traceback String",
            )
        )

    async def async_post_call_success_hook(
        self,
        data: dict,
        user_api_key_dict: UserAPIKeyAuth,
        response: LLMResponseTypes,
    ) -> Any:
        # data is the original request data
        # response is the response from the LLM API
        _console.print(
            Panel(
                Pretty(response.choices[0].message),
                title="Post Call Success Hook - Response",
            )
        )

    async def async_post_call_streaming_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        response: str,
    ) -> Any:
        _console.print(
            Panel(
                Pretty(response),
                title="Streaming response received",
            )
        )


proxy_handler_instance = MyCustomHandler()
