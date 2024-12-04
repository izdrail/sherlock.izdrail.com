import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


from api.endpoints import security

app = FastAPI(
    title="Security App",
    description="Protect your family members from the worst possible cyber attacks with our o.s.i.n.t. solution",
    version="0.0.1",
    terms_of_service="https://security.izdrail.com/terms",

    contact={
        "name": "Stefan Bogdanel",
        "url": "https://security.izdrail.com/",
        "email": "stefan@izdrail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# TODO - Simplify and improve code

# Endpoints
#app.include_router(nlp.router)
#app.include_router(google.router)
#app.include_router(feeds.router)
#app.include_router(seo.router)
#app.include_router(videos.router)
#app.include_router(social.router)
#app.include_router(jobs.router)
#app.include_router(scrapper.router)
app.include_router(security.router)

print("Starting server on port 8003")

import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi_versioning import VersionedFastAPI, version

from api.endpoints import security

# Initialize FastAPI app
app = FastAPI(
    title="Social Guard API",
    description="Protect your family members from the worst possible cyber attacks with Social Guard API",
    terms_of_service="https://security.izdrail.com/terms",
    contact={
        "name": "Stefan Bogdanel",
        "url": "https://security.izdrail.com/",
        "email": "stefan@izdrail.com",
    },
    license_info={
        "name": "Apache 2.0",
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

app = VersionedFastAPI(app,version_format='{major}')

@app.get("/")
async def root():
    return {"message": "Welcome to the Security API! check /v1_0/docs for more information."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10001, reload=True)