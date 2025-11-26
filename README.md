# Riot Take-Home Technical Challenge
## Overview

For this take-home challenge, I built an HTTP API with 4 endpoints that handle JSON payloads for encryption, decryption, signing, and verification operations.

## Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **Testing**: pytest

## Setup Instructions

### Clone Repository
```bash
git clone https://github.com/diegomonteagudo/riot-take-home
cd repository
```

### Create Virtual Environment (optional)
```bash
python -m venv venv
```

### Activate Virtual Environment (optional)

#### Linux/macOS
```bash
source venv/bin/activate
```

Windows (Command Prompt)
```cmd
venv\Scripts\activate.bat
```

Windows (PowerShell)
```powershell
venv\Scripts\Activate.ps1
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
fastapi run app/main.py
```

The server will start on `http://localhost:8000`

**Note** : There is also the OpenAPI specification available at `http://localhost:8000/docs` where you can read the documentation and run examples.

### Running the tests
```bash
pytest
```

## API Endpoints

### POST `/encrypt`
Encrypts all properties at the first depth using Base64 encoding.

### POST `/decrypt`
Decrypts Base64 encoded properties, leaving non-encrypted values unchanged.

### POST `/sign`
Generates an HMAC signature for the provided JSON payload (order-independent).

### POST `/verify`
Verifies a signature against provided data.
- Returns 204 (No Content) on success
- Returns 400 (Bad Request) on invalid signature

## Project Structure

```
riot-take-home/
├── README.me
├── requirements.txt         # Python dependencies
├── app/                     # Main application code
│   ├── __init__.py
│   ├── config.py            # Configuration (HMAC key)
│   ├── endpoints.py         # Endpoint definitions
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # Pydantic models
│   └── core/                # Core logic and abstractions
│         ├── encryption_strategies.py  # Strategy pattern for encryption
│         ├── signing_strategies.py     # Strategy pattern for signing
│         └── utils.py                  # Utility functions
└── tests/                   # Integration tests
```


## Design Decisions

### Framework choice
I used FastAPI because of :
- the gain in development speed compared to the scope of this project in particular
- the automatic OpenAPI documentation
- the Pydantic data models
- the reliance of FastAPI on type hints making development both more efficient (request validation) and reliable
- its speed compared to other Python frameworks

I also hesitated with Node.js with Express because I know Riot uses TypeScript on the front-end, but ultimately decided to go with FastAPI because of the scope of the challenge

### Abstractions
- Implemented the Strategy design pattern for easy algorithm swapping
- For encryption/decryption, `EncryptionStrategy` is the abstract class. It is implemented with Base64 as the encryption algorithm with `Base64EncryptionStrategy`
- For encryption/decryption, `SigningStrategy` is the abstract class. It is implemented with Base64 as the encryption algorithm with `HMACSigningStrategy`

### Signature Algorithm
The key for the HMAC algorithm is available in app/config.py. In a real production environment, this key would be a secure secret stored in environment variables or a secrets manager.

### Error Handling
- It was not explicitely stated how the API should answer in case of invalid or missing JSONs
- Error 400 is an actual intended possible output of the API in case of an invalid signature in `/verify`
- FastAPI's automatic request validation (using Pydantic data models) use error 422 in case of an invalid request

For these reasons, I decided 422 was an adequate response in case of invalid JSONs and bodies with no JSON at all.


### Detection of unencrypted data (`/decrypt`)
To detect whether or not a specific property is encrypted, I simply try json.loads and see if it fails. However, it has come to my mind that there may exist non-Base64 strings that decode as valid Base64 into an integer or a boolean. 

Here are two ideas of how to do it differently :
- in a stochastic manner by studying how much the succession of characters matches the profile of a Base64 encoding
- by encoding not only the value itself but its type in a new JSON object

### Testing

The tests are available in the `tests` folder. You can run them with the `pytest` command.

They were all written before the feature they test for, following a TDD methodology. They test for invalid or empty JSONs, different types, attribute order, nested objects and cycles (`/encrypt` followed by `/decrypt` and `/sign` followed by `/verify`).

**Note:** I realize my solution lacks unit tests. I decided to only go with integration tests because of the time constraint and the relatively small size of the project.


### OpenAPI documentation
FastAPI generated an OpenAPI documentation available at `http://localhost:8000/docs` after launching the server. It uses Swagger UI, you can manually test JSON objects.