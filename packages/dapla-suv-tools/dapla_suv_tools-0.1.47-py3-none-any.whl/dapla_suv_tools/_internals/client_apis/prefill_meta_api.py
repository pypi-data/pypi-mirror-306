import json
import os

from dapla_suv_tools._internals.integration.api_client import SuvApiClient
from dapla_suv_tools._internals.util.operation_result import OperationResult
from dapla_suv_tools._internals.util.suv_operation_context import SuvOperationContext
from dapla_suv_tools._internals.util import constants
from dapla_suv_tools._internals.util.validators import (
    skjema_id_validator,
)
from dapla_suv_tools._internals.util.decorators import result_to_dict


END_USER_API_BASE_URL = os.getenv("SUV_END_USER_API_URL", "")

client = SuvApiClient(base_url=END_USER_API_BASE_URL)


@result_to_dict
@SuvOperationContext(validator=skjema_id_validator)
def get_prefill_meta_by_id(
    self, *, skjema_id: int, context: SuvOperationContext
) -> OperationResult:
    """
    Gets prefill meta for a 'skjema' based on it's skjema_id.

    Parameters:
    ------------
    skjema_id: int, required
        The skjema_id associated with the new period.
    context: SuvOperationContext
        Operation context for logging and error handling. This is injected by the underlying pipeline.

    Returns:
    --------
    OperationResult:
        A list of json objects containing the skjema's prefill meta data

    Example:
    ---------
    result = get_prefill_meta_by_id(
        skjema_id=123
    )
    """

    try:
        content: str = client.get(
            path=f"{constants.PREFILL_META_PATH}/{skjema_id}", context=context
        )
        content_json = json.loads(content)
        # context.log(constants.LOG_INFO, "get_skjema_by_id", f"Fetched 'skjema' with id '{skjema_id}'")
        context.log(message="Fetched 'skjema' with id '{skjema_id}'")
        return OperationResult(value=content_json, log=context.logs())

    except Exception as e:
        context.set_error(f"Failed to fetch for id {skjema_id}", e)
        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )
