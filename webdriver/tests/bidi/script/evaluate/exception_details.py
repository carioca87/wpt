import pytest
from webdriver.bidi.modules.script import ContextTarget, ScriptEvaluateResultException

from ... import any_int, any_string, recursive_compare
from .. import any_stack_trace
from . import PRIMITIVE_AND_REMOTE_VALUES


@pytest.mark.asyncio
@PRIMITIVE_AND_REMOTE_VALUES
async def test_exception_details(bidi_session, top_context, expression,
                                 expected):
    with pytest.raises(ScriptEvaluateResultException) as exception:
        await bidi_session.script.evaluate(
            expression=f"throw {expression}",
            target=ContextTarget(top_context["context"]),
            await_promise=False,
        )

    recursive_compare(
        {
            "realm": any_string,
            "exceptionDetails": {
                "columnNumber": any_int,
                "exception": expected,
                "lineNumber": any_int,
                "stackTrace": any_stack_trace,
                "text": any_string,
            },
        },
        exception.value.result,
    )
