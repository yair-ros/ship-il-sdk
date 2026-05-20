from tenacity import retry, stop_after_attempt, wait_exponential


@retry(
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(5),
)
def retryable(func, *args, **kwargs):
    return func(*args, **kwargs)
