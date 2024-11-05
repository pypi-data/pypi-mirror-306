from typing import Any, Dict, List, Optional, Sequence

import requests
from requests.exceptions import HTTPError

from snarkify_cli.lib.auth import get_auth_header
from snarkify_cli.lib.constants import (
    ADD_SERVICE_DATA_ITEM_URL,
    CATALOG_URL,
    CREATE_IMAGE_URL_TEMPLATE,
    CREATE_SERVICE_DATA_URL,
    CREATE_SERVICE_URL,
    DEPLOY_SERVICE_URL_TEMPLATE,
    DEPLOYMENT_URL,
    DEV_SHELL_URL,
    LIST_SERVICE_DATA_ITEM_URL,
    LIST_SERVICE_DATA_URL_TEMPLATE,
    LIST_TEAM_URL,
    NAMESPACE_URL,
    SERVICE_URL,
    TASK_URL,
)


def get_teams() -> List[Dict[str, str]]:
    response = requests.get(LIST_TEAM_URL, headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def create_service(name: str, team_id: str, sku_id: str, price_id: str) -> str:
    params = dict(name=name, team_id=team_id, sku_id=sku_id, price_id=price_id)
    response = requests.post(CREATE_SERVICE_URL, headers=get_auth_header(), json=params)
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()["service_id"]


def get_service(service_id: str) -> Dict[str, Any]:
    response = requests.get(f"{SERVICE_URL}/{service_id}", headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def list_services(team_id: str) -> List[Dict[str, Any]]:
    namespace_response = requests.get(f"{NAMESPACE_URL}?team_id={team_id}", headers=get_auth_header())
    if not namespace_response.ok:
        detail = namespace_response.json()["detail"]
        raise HTTPError(f"Error({namespace_response.status_code}): {detail}", response=namespace_response)
    namespace_json = namespace_response.json()
    if len(namespace_json) != 1:
        # We don't support multiple namespaces for now.
        # TODO: We need some tools/libararies to report exceptions to our server from client side.
        pass
    namespace_id = namespace_json[0]["namespace_id"]
    response = requests.get(f"{SERVICE_URL}?namespace_id={namespace_id}", headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def create_task(service_id: str, params: Dict[str, Any]) -> str:
    response = requests.post(f"{SERVICE_URL}/{service_id}", json=params, headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()["task_id"].strip()


def get_task(task_id: str) -> Dict[str, Any]:
    response = requests.get(f"{TASK_URL}/{task_id}", headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def create_service_image(service_id: str, tag: str) -> Dict[str, Any]:
    params = dict(tag=tag)
    response = requests.post(CREATE_IMAGE_URL_TEMPLATE.format(service_id), headers=get_auth_header(), json=params)
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def deploy_service(service_id: str, image_id: str) -> Dict[str, Any]:
    params = dict(image_id=image_id)
    response = requests.post(DEPLOY_SERVICE_URL_TEMPLATE.format(service_id), headers=get_auth_header(), json=params)
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def update_service_env_vars(service_id: str, env_vars: Dict[str, Optional[str]]) -> Dict[str, Any]:
    params = dict(env_vars=env_vars)
    response = requests.put(f"{SERVICE_URL}/{service_id}", headers=get_auth_header(), json=params)
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def get_linked_service_data(service_id: str) -> Optional[str]:
    response = requests.get(LIST_SERVICE_DATA_URL_TEMPLATE.format(service_id), headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    for data in response.json():
        if data["state"] == "ACTIVE":
            # on the server side we only allow 1 linked data, so just return it here
            return data["data_id"]
    return None


def create_service_data(team_id: str, service_id: str) -> str:
    params = dict(team_id=team_id, service_id=service_id)
    response = requests.post(CREATE_SERVICE_DATA_URL, headers=get_auth_header(), json=params)
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()["data_id"]


def get_service_data_upload_urls(data_id: str, files: Sequence[str]) -> Dict[str, str]:
    params = dict(files_to_add=files)
    response = requests.post(ADD_SERVICE_DATA_ITEM_URL.format(data_id), headers=get_auth_header(), json=params)
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()["files_to_add_map"]


def list_service_data_items(data_id: str) -> Sequence[Dict[str, str]]:
    response = requests.get(LIST_SERVICE_DATA_ITEM_URL.format(data_id), headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()["items"]


def create_shell(team_id: str, name: Optional[str], sku_id: str, price_id: str, image_display_name: str) -> str:
    response = requests.post(
        DEV_SHELL_URL,
        json={
            "name": name,
            "team_id": team_id,
            "sku_id": sku_id,
            "price_id": price_id,
            "image_display_name": image_display_name,
        },
        headers=get_auth_header(),
    )
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()["shell_id"].strip()


def start_shell(shell_id: str) -> Dict[str, str]:
    response = requests.post(
        f"{DEV_SHELL_URL}/{shell_id}/starts",
        headers=get_auth_header(),
    )
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def stop_shell(shell_id: str) -> Dict[str, str]:
    response = requests.post(
        f"{DEV_SHELL_URL}/{shell_id}/stops",
        headers=get_auth_header(),
    )
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def delete_shell(shell_id: str) -> None:
    response = requests.delete(
        f"{DEV_SHELL_URL}/{shell_id}",
        headers=get_auth_header(),
    )
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)


def get_shell(shell_id: str) -> Dict[str, str]:
    response = requests.get(
        f"{DEV_SHELL_URL}/{shell_id}",
        headers=get_auth_header(),
    )
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def list_shells(team_id: str) -> Sequence[Dict[str, str]]:
    response = requests.get(
        f"{DEV_SHELL_URL}?team_id={team_id}",
        headers=get_auth_header(),
    )
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def get_catalogs(team_id: str) -> Dict[str, Any]:
    response = requests.get(f"{CATALOG_URL}/teams/{team_id}", headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def get_shell_images() -> Sequence[Dict[str, Any]]:
    response = requests.get(f"{DEV_SHELL_URL}/images")
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def get_deployment(deployment_id: str) -> Dict[str, Any]:
    response = requests.get(f"{DEPLOYMENT_URL}/{deployment_id}", headers=get_auth_header())
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()


def list_deployments(service_id: str, page: int, size: int) -> Dict[str, Any]:
    response = requests.get(
        f"{DEPLOYMENT_URL}?service_id={service_id}&page={page}&size={size}", headers=get_auth_header()
    )
    if not response.ok:
        detail = response.json()["detail"]
        raise HTTPError(f"Error({response.status_code}): {detail}", response=response)
    return response.json()
