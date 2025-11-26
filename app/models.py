from pydantic import BaseModel

EXAMPLE_SIGNATURE = "5516a423840ead999d396582e508cfc53ea974dc9924b3cb597059da942900d4"


class SignatureResponse(BaseModel):
    """Pydantic data model for the response of the /sign endpoint"""

    signature: str

    class Config:  # For the OpenAPI documentation
        schema_extra = {"example": {"signature": EXAMPLE_SIGNATURE}}


class VerifyRequest(BaseModel):
    """Pydantic data model for the request of the /verify endpoint"""

    signature: str
    data: dict

    class Config:  # For the OpenAPI documentation
        schema_extra = {
            "example": {
                "signature": "{}".format(EXAMPLE_SIGNATURE),
                "data": {"message": "Hello World", "timestamp": 1616161616},
            }
        }
