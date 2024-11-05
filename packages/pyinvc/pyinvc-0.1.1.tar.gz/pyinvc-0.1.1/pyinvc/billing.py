import json
from datetime import timedelta, datetime
from typing import List, Dict, Tuple


class BillingService:
    cycle = {
        "0": "one_time",
        "1": "1m",
        "3": "3m",
        "6": "6m",
        "12": "1y",
        "24": "2y",
        "36": "3y",
        "48": "4y",
        "60": "5y",
        "72": "6y",
        "84": "7y",
        "96": "8y",
        "108": "9y",
        "120": "10y",
    }

    def __init__(self, *, base_url: str = None, secret_token: str = None, user_id: int, filters: str = None):
        self.BASE_URL = base_url or config("BILLING_BASE_URL")
        self.HEADER = {
            "Authorization": secret_token or f"Bearer {config("BILLING_SECRET_TOKEN")}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.user_id = user_id

        if filters and not isinstance(filters, str):
            raise ValueError("The filters must be string type.")

        self.filters = f"&{filters}" if filters else ""

    def invoice_list(self) -> Json:
        try:
            response = requests.request(
                method="GET",
                url=f"{self.BASE_URL}/invoice?filters[business_user_id][$eq]={self.user_id}{self.filters}",
                headers=self.HEADER,
            )
            response.raise_for_status()
            res_json = response.json()
            return res_json
        except (JSONDecodeError, RequestException) as ex:
            raise ValueError(ex)

    def invoice_detail(self, invoice_id) -> Json:
        try:
            response = requests.request(
                method="GET",
                url=f"{self.BASE_URL}/invoice/{invoice_id}?filters[business_user_id][$eq]={self.user_id}{self.filters}",
                headers=self.HEADER,
            )
            response.raise_for_status()
            res_json = response.json()
            return res_json
        except (JSONDecodeError, RequestException) as ex:
            raise ValueError(ex)

    @staticmethod
    def _apply_invoice_item_promotions(items: List[int]):
        if not items:
            return []
        promotion_objs = ProductPromotionModel.objects.filter(id__in=items)
        return [
            {
                "type": "promotion_percent" if promotion_obj.is_percent else "promotion_fixed",
                "description": promotion_obj.code,
                "cycle": 0,
                "amount": promotion_obj.amount,
                "currency": "IRR",
                "product": "promotion",
            }
            for promotion_obj in promotion_objs
        ]

    def _apply_invoice_items(self, items: List[Dict]) -> List[Dict]:
        invoice_item = []
        for index, item in enumerate(items):
            if pp_id := item.get("product_price_id"):
                pp_obj = ProductPriceModel.objects.filter(pk=pp_id).first()
                resource_data = {
                    i["key"]: i["value"] for i in
                    ProductPriceMetadataModel.objects.filter(price=pp_obj).values("key", "value") if
                    i["key"] in ["storage", "count"]
                }
                invoice_item.append({
                    "pp_id": pp_id,
                    "plan_id": item["plan_id"],
                    "domain": None,
                    "product": "service",
                    "kind": item["kind"],
                    "period": pp_obj.period,
                    "type": "product",
                    "description": item.get("description"),
                    "cycle": self.cycle[str(pp_obj.period)],
                    "amount": pp_obj.amount * 10,
                    "currency": "IRR",
                    "start_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "rel_id": index + 1,  # billing api does not accept 0 as rel_id
                    "addons": [
                        {
                            "type": "addon",
                            "description": json.dumps({
                                "plan_name": pp_obj.product.name,
                                "storage": resource_data["storage"],
                                "count": resource_data["count"],
                                "country": "Germany",
                            })
                        }
                    ]
                })
            elif domain := item.get("domain"):

                if item["domain"].endswith(".ir"):
                    domain_amount = get_irnic_domain_price(
                        domain=domain,
                        period=int(int(item["cycle"]) / 12),
                        kind=item["kind"]
                    )
                else:
                    domain_amount = get_joker_domain_price(
                        user_domain=domain,
                        period=int(int(item["cycle"]) / 12),
                        kind=item["kind"]
                    )
                invoice_item.append({
                    "pp_id": None,
                    "plan_id": None,
                    "domain": item["domain"],
                    "product": "domain",
                    "kind": item["kind"],
                    "period": int(item["cycle"]),
                    "contact": item["contact"],
                    "ns_list": item["ns_list"],
                    "epp_code": item["epp_code"],
                    "type": "domain",
                    "description": item.get("description"),
                    "cycle": self.cycle[item["cycle"]],
                    "amount": domain_amount * 10,
                    "currency": "IRR",
                    "start_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    "rel_id": index + 1,  # billing api does not accept 0 as rel_id
                    "addons": [
                        {
                            "type": "addon",
                            "description": json.dumps({
                                "domain": item["domain"],
                            })
                        }
                    ]
                })
        return invoice_item

    def invoice_create(self, items: List[Dict]) -> Tuple[List[Dict], Json]:
        items = self._apply_invoice_items(items=items)
        items.append({
            "type": "tax",
            "description": "مالیات بر ارزش افزوده",
            "amount": 10,
            "product": "tax",
        })
        try:
            response = requests.request(
                method="POST",
                url=f"{self.BASE_URL}/invoice",
                headers=self.HEADER,
                json={
                    "user_id": self.user_id,
                    "duedate": (now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S"),
                    "items": items
                }
            )
            response.raise_for_status()
            res_json = response.json()
            return items, res_json
        except (JSONDecodeError, RequestException) as ex:
            raise ValueError(ex)

    def invoice_add_promotion(self, invoice_id: int, promotion_data: dict) -> Json:
        try:
            response = requests.request(
                method="POST",
                url=f"{self.BASE_URL}/item/{invoice_id}",
                headers=self.HEADER,
                json={
                    "items": [promotion_data]
                }
            )
            response.raise_for_status()
            res_json = response.json()
            return res_json
        except (JSONDecodeError, RequestException) as ex:
            raise ValueError(ex)

    def payment(self, invoice_id: int) -> str:
        try:
            response = requests.request(
                method="POST",
                url=f"{self.BASE_URL}/payment/{invoice_id}",
                headers=self.HEADER,
                json={
                    "callback_url": f"{config("BILLING_CALLBACK_URL")}/{invoice_id}",
                }
            )
            response.raise_for_status()
            res_json = response.text
            return res_json
        except (JSONDecodeError, RequestException) as ex:
            raise ValueError(ex)

    def invoice_delete_item(self, invoice_id, item_id) -> None:
        try:
            response = requests.request(
                method="DELETE",
                url=f"{self.BASE_URL}/item/{invoice_id}/{item_id}",
                headers=self.HEADER,
            )
            response.raise_for_status()
            res_json = response.json()
            return None
        except (JSONDecodeError, RequestException) as ex:
            raise ValueError(ex)

    def settle(self, invoice_id: str) -> Json:
        try:
            response = requests.request(
                method="POST",
                url=f"{self.BASE_URL}/invoice/settel",
                headers=self.HEADER,
                json={"invoice_id": invoice_id}
            )
            response.raise_for_status()
            res_json = response.json()
            return res_json
        except (JSONDecodeError, RequestException) as ex:
            raise ValueError(ex)

    def transaction_list(self, invoice_id) -> Json:
        try:
            response = requests.request(
                method="GET",
                url=f"{self.BASE_URL}/transaction?filters[invoice_id][$eq]={invoice_id}",
                headers=self.HEADER,
            )
            response.raise_for_status()
            res_json = response.json()
            return res_json
        except (JSONDecodeError, RequestException) as ex:
            raise ValueError(ex)
