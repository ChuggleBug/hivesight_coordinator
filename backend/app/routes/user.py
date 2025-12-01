
# Routes to be used by the user

from fastapi import APIRouter, Body, status, HTTPException
from typing import Dict, List
from ..models.mapping import NetworkDevices
import requests
from ..models.config import settings
from ..models.userauth import UserAuth

router = APIRouter(
    tags=["User"]
)


@router.post("/config/assoc", status_code=status.HTTP_204_NO_CONTENT, summary="Update sensor-to-device associations")
def config_device_assoc(
    assoc: Dict[str, List[str]] = Body(
        ...,
        example={
            "button": ["patio", "fence"],
            "door": ["kitchen"]
        },
        description="Mapping of sensor names to lists of associated device names"
    )
):
    print(f"Updating sensor mappings: {assoc}")
    if NetworkDevices.set_sensor_mappings(assoc):
        # Notify all known cameras to update their mappings
        for camera in NetworkDevices.get_camera_devices():
            NetworkDevices.message_mappings_to_camera(camera)
        return status.HTTP_204_NO_CONTENT

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Trying to create associations to devices that don't exist"
    )


@router.get("/config/assoc", status_code=status.HTTP_200_OK, summary="Get sensor-to-device associations")
def get_device_assoc():
    return NetworkDevices.get_sensor_mappings()


@router.get("/devices")
def get_devices():
    return {
        "sensors": NetworkDevices.get_sensor_devices(),
        "cameras": NetworkDevices.get_camera_devices()
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Indicate to the coordinator to logout")
def coordinator_logout():
    print("Logging the coordinator out")
    UserAuth.set_auth({
        "user": "",
        "token": ""
    })


@router.post("/login", status_code=status.HTTP_200_OK, summary="Login coordinator via cloud API")
def route_login(
    auth: Dict[str, str] = Body(
        ...,
        example={
            "username": "user",
            "password": "pass"
        },
        description="Username and password used to authenticate the coordinator with the cloud account"
    )
):
    try:
        resp = requests.post(
            f"http://{settings.cloud_hostname}:{settings.cloud_port}/api/user/login",
            json={
                "username": auth["username"],
                "password": auth["password"]
            })
    except requests.RequestException:
        print(f"Error contacting cloud login API")
        raise HTTPException(
            status_code=500, detail="Cloud Service Down")
    except KeyError:
        raise HTTPException(
            status_code=500, detail="Missing Parameters")

    if resp.ok:
        auth_resp: Dict[str, str] = resp.json()
        UserAuth.set_auth(
            {"user": auth["username"], "token": auth_resp["token"]})
        return auth_resp
    else:
        try:
            error_data = resp.json()
        except ValueError:
            error_data = "Unkown Cloud Error"

        raise HTTPException(status_code=resp.status_code, detail=error_data)


@router.get("/sync", status_code=status.HTTP_200_OK, description="Returns what auth information the coordinator has. Used to ensure that both the user and the backend have the same authentication")
def sync_account():
    # Call validate to ensure current token is valid
    if len(UserAuth.get_auth()["token"]) != 0:
        try:
            resp = requests.post(
                f"http://{settings.cloud_hostname}:{settings.cloud_port}/api/user/validate", json=UserAuth.get_auth())
        except requests.RequestException:
            print(f"Error contacting cloud login API")
            raise HTTPException(
                status_code=500, detail="Failed to contact cloud login API")
        except KeyError:
            raise HTTPException(
                status_code=500, detail="Invalid parameters provided")

        data = resp.json()
        # Current auth is not longer valid
        if not data["valid"]:
            print("token no longer valid")
            UserAuth.set_auth({
                "user": "",
                "token": ""
            })

    return UserAuth.get_auth()
