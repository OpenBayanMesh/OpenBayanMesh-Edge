from fastapi import Header, HTTPException, status
from typing import Optional

async def get_api_version(accept_version: Optional[str] = Header(None)):
    if accept_version:
        # In a real application, you would validate this against a list of supported versions
        supported_versions = ["v1"]
        if accept_version not in supported_versions:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"API version '{accept_version}' is not supported. Supported versions are: {', '.join(supported_versions)}."
            )
    return accept_version
