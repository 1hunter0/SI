from fastapi import APIRouter


router = APIRouter()

@router.get("/url/{url}")
async def getURL(url):
    return {}


@router.get("/ip/{ip}")
async def getURL(ip):
    return {}


@router.get("/dns/{dns}")
async def getURL(ip):
    return {}


@router.get("/file/{file}")
async def getURL(file):
    return {}
