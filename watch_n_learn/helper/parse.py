from typing import Dict, List, Optional
from urllib.parse import parse_qs

from fastapi.requests import Request

async def body_as_json(
    request: Request, parameters: List[str]
) -> Optional[Dict[str, str]]:

    body = parse_qs((await request.body()).decode("utf-8"), True)

    for parameter in parameters:
        if parameter not in body:

            return None

    return {key: value[0] for key, value in body.items()}
