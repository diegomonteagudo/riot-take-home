from pydantic import BaseModel

class SignatureResponse(BaseModel):
    """ Pydantic data model for the response of the /sign endpoint """
    signature: str


class VerifyRequest(BaseModel):
    """ Pydantic data model for the request of the /verify endpoint """
    signature: str
    data: dict