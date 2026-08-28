import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi_versioning import VersionedFastAPI, version

from api.endpoints import security, assistant

# Initialize FastAPI app
app = FastAPI(
    title="Sherlock - OSINT API",
    description="Protect your family members from the worst possible cyber attacks with Sherlock Guard API",
    terms_of_service="https://izdrail.com/terms",
    contact={
        "name": "Stefan Bogdanel",
        "url": "https://izdrail.com/",
        "email": "stefan@izdrail.com",
    },
    license_info={
        "name": "CC BY 4.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Router inclusion
app.include_router(security.router)
app.include_router(assistant.router)

app = VersionedFastAPI(app, version_format='{major}')

@app.get("/")
async def root():
    return {"message": "Welcome to the Security API! check /v1_0/docs for more information."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10001, reload=True)
