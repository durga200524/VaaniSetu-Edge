import json

from pathlib import Path
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/api/v1/resolution",
    tags=["Resolution Passport"]
)


# Resolution Passport storage directory
BASE_DIR = Path(__file__).resolve().parents[2]

PASSPORT_DIR = (
    BASE_DIR / "data" / "resolution_passports"
)


@router.get("/all")
async def get_all_passports():

    PASSPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    passports = []

    for file_path in PASSPORT_DIR.glob("*.json"):

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                passport = json.load(file)

                passports.append(passport)

        except (json.JSONDecodeError, OSError):
            continue

    return {
        "success": True,
        "total_passports": len(passports),
        "passports": passports
    }


@router.get("/{passport_id}")
async def get_passport(passport_id: str):

    file_path = PASSPORT_DIR / f"{passport_id}.json"

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Resolution Passport not found."
        )

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            passport = json.load(file)

        return {
            "success": True,
            "passport": passport
        }

    except (json.JSONDecodeError, OSError):
        raise HTTPException(
            status_code=500,
            detail="Unable to read Resolution Passport."
        )