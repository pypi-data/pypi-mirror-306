from typing import Tuple
from snarkify_cli.lib.http_utils import get_catalogs
from snarkify_cli.lib.prompt_utils import prompt_for_selection, PROMPT_SELECTION_TYPE
from snarkify_cli.lib.errors import NoSkuError


def select_service_sku_price(team_id: str) -> Tuple[str, str]:
    catalogs = get_catalogs(team_id)
    service_sku_prices = catalogs.get("service")
    if not service_sku_prices:
        raise NoSkuError("No SKUs available.")
    selected_catalog_idx = prompt_for_selection(
        [sku_price["sku"]["display_name"] for sku_price in service_sku_prices], PROMPT_SELECTION_TYPE.CATALOG
    )
    selected_sku_price = service_sku_prices[selected_catalog_idx]
    sku_display_name = selected_sku_price["sku"]["display_name"]
    print(f"You've selected {sku_display_name} for your service.")
    return selected_sku_price["sku"]["sku_id"], selected_sku_price["unit_price"]["price_id"]
