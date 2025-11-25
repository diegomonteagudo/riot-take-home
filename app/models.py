from pydantic import BaseModel

class SignatureResponse(BaseModel):
    """ Pydantic data model for the response of the /sign endpoint """
    signature: str