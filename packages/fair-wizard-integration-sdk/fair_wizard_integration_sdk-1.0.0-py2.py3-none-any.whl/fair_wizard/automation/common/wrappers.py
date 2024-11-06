import os
import func_timeout

from .model import ErrorResponse, IHandler, HandlerContext


def make_handler(func) -> IHandler:
    def handler(event: dict, context: HandlerContext) -> dict:
        if 'TIMEOUT' in os.environ:
            timeout = float(os.environ['TIMEOUT'])
        else:
            remaining_ms = context.get_remaining_time_in_millis()
            timeout = remaining_ms / 1000 - 1
        try:
            result = func_timeout.func_timeout(
                timeout=timeout,
                func=func,
                args=(event, context),
                kwargs=None,
            )
            return result.serialize()
        except func_timeout.exceptions.FunctionTimedOut:
            return ErrorResponse(
                message='Processing exceeded time limit (1 second)',
            ).serialize()
        except Exception as e:
            return ErrorResponse(
                message=f'Error when using custom automation: '
                        f'{e.__class__.__name__}: {str(e)}',
            ).serialize()
    return handler


def make_error_handler(exception: BaseException) -> IHandler:
    def handler(event: dict, context: HandlerContext) -> dict:
        return ErrorResponse(
            message=f'Error when importing custom automation: '
                    f'{exception.__class__.__name__} ({str(exception)})',
        ).serialize()
    return handler
