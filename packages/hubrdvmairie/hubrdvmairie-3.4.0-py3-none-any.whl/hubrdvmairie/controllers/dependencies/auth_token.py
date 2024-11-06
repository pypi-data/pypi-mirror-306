import json
import os

from fastapi import Header, HTTPException, Request


async def verify_auth_token(request: Request, x_hub_rdv_auth_token: str = Header(None)):
    """
    Verify the authentication token provided in the X-HUB-RDV-AUTH-TOKEN header.

    Args:
        request (Request): The incoming request object.
        x_hub_rdv_auth_token (str, optional): The value of the X-HUB-RDV-AUTH-TOKEN header. Defaults to None.

    Raises:
        HTTPException: If the X-HUB-RDV-AUTH-TOKEN header is invalid.

    """
    if request.headers.get("X-HUB-RDV-FRONT-AUTH-TOKEN") in json.loads(
        os.environ.get("FRONT_AUTH_TOKENS")
    ):
        return
    if x_hub_rdv_auth_token not in json.loads(os.environ.get("AUTH_TOKENS")):
        raise HTTPException(
            status_code=401, detail="X-HUB-RDV-AUTH-TOKEN header invalid"
        )


async def verify_internal_auth_token(
    request: Request, x_hub_rdv_internal_auth_token: str = Header(None)
):
    """
    Verify the internal authentication token provided in the X-HUB-RDV-INTERNAL-AUTH-TOKEN header.

    Args:
        request (Request): The incoming request object.
        x_hub_rdv_internal_auth_token (str, optional): The value of the X-HUB-RDV-INTERNAL-AUTH-TOKEN header. Defaults to None.

    Raises:
        HTTPException: If the X-HUB-RDV-INTERNAL-AUTH-TOKEN header is invalid.

    """
    if os.environ.get("ADMIN_AUTH_TOKENS"):
        if x_hub_rdv_internal_auth_token in json.loads(
            os.environ.get("ADMIN_AUTH_TOKENS")
        ):
            request.state.editor_name = "RDV-DATA-ADMIN"
        else:
            raise HTTPException(
                status_code=401, detail="X-HUB-RDV-INTERNAL-AUTH-TOKEN header invalid"
            )


async def verify_front_auth_token(
    request: Request, x_hub_rdv_front_auth_token: str = Header(None)
):
    """
    Verify the front authentication token provided in the X-HUB-RDV-FRONT-AUTH-TOKEN header.

    Args:
        request (Request): The incoming request object.
        x_hub_rdv_front_auth_token (str, optional): The value of the X-HUB-RDV-FRONT-AUTH-TOKEN header. Defaults to None.

    Raises:
        HTTPException: If the X-HUB-RDV-FRONT-AUTH-TOKEN header is invalid.

    """
    if x_hub_rdv_front_auth_token not in json.loads(
        os.environ.get("FRONT_AUTH_TOKENS")
    ):
        raise HTTPException(
            status_code=401, detail="X-HUB-RDV-FRONT-AUTH-TOKEN header invalid"
        )
