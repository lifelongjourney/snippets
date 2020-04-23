import logging
import time
from functools import wraps
from typing import Callable


def repeat(
    f_evaluate_result: Callable[[object], bool] = lambda arg: arg or False,
    f_get_summary: Callable[[object], str] = lambda arg: str(arg),
    raise_on_timeout: bool = True,
    delay: int = 60,
    max_repeats: int = 60,
    logger: logging = None,
    tag: str = "repeat"
) -> Callable:
    """
    Retry calling the decorated function till of which result is evaluated true by the given evaluation function
    Args:
        :param f_evaluate_result: function to evaluate the result of decorated function
        :param f_get_summary: function to get one line summary of result
        :param delay: Initial delay between retries in seconds.
        :param max_repeats: maximum number of times to retry
        :param raise_on_timeout: raise an exception when it hits the wait_threshold
        :param logger: Logger to use. If None, print.
        :param tag: hint for the action to be repeated
    """

    def decorator(f):
        @wraps(f)
        def f_repeat_until(*args, **kwargs):
            repeated = 0
            while True:
                last_result = f(*args, **kwargs)
                last_eval = f_evaluate_result(last_result)
                last_eval_summary = f_get_summary(last_result)
                repeated += 1
                if last_eval or repeated >= max(max_repeats, 1):
                    break

                msg = f"evaluation({tag}) failed" \
                      f", will repeat after {delay}s, repeated {repeated} / {max_repeats}" \
                      f", last evaluation : {last_eval_summary}"
                logger.debug(msg) if logger else print(msg)
                time.sleep(delay)

            if last_eval:
                return last_result

            msg = "{%s} failed after max-repeats repeated : %s times, last-evaluation : %s" % (
                tag, repeated, last_eval_summary
            )
            logger.warn(msg) if logger else print(msg)
            if raise_on_timeout and not last_eval:
                raise Exception(msg)

            return last_result

        return f_repeat_until

    return decorator


def _test():
    repeat(tag="test-1", max_repeats=1, delay=1)(lambda: True)()
    repeat(tag="test-2", max_repeats=2, delay=1)(lambda: True)()
    repeat(tag="test-3", max_repeats=1, delay=1, raise_on_timeout=False)(lambda: False)()
    repeat(tag="test-4", max_repeats=1, delay=1, raise_on_timeout=True)(lambda: False)()


if __name__ == '__main__':
    _test()
