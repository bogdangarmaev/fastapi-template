import httpx
from httpx import BasicAuth


def initialize_host(url_base: str, secure_connection: bool) -> str:
    if secure_connection:
        prefix = "https://"
    else:
        prefix = "http://"

    if url_base[0:4] == "http":
        raise ValueError(
            f"Хост [{url_base}] не может начинаться с http/https."
        )

    host = f"{prefix}{url_base}"

    if host[-1] != "/":
        host += "/"

    return host


async def make_api_request(
    url: str, auth: BasicAuth = None, params: dict = None, verify: bool = False
):
    if params is None:
        params = {}

    async with httpx.AsyncClient(verify=verify) as client:
        response = await client.get(url, auth=auth, params=params)
        response.raise_for_status()
        return response
