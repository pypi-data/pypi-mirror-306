#
#  Copyright MindBridge Analytics Inc. all rights reserved.
#
#  This material is confidential and may not be copied, distributed,
#  reversed engineered, decompiled or otherwise disseminated without
#  the prior written consent of MindBridge Analytics Inc.
#

from dataclasses import dataclass
from functools import cached_property
import logging
from typing import TYPE_CHECKING, Any, Optional
from mindbridgeapi.account_group_item import AccountGroupItem
from mindbridgeapi.base_set import BaseSet
from mindbridgeapi.exceptions import ItemNotFoundError, ParameterError
from mindbridgeapi.generated_pydantic_model.model import MindBridgeQueryTerm

if TYPE_CHECKING:
    from collections.abc import Generator

logger = logging.getLogger(__name__)


@dataclass
class AccountGroups(BaseSet):
    @cached_property
    def base_url(self) -> str:
        return f"{self.server.base_url}/account-groups"

    def get_by_id(self, id: str) -> AccountGroupItem:
        url = f"{self.base_url}/{id}"
        resp_dict = super()._get_by_id(url=url)

        return AccountGroupItem.model_validate(resp_dict)

    def get(
        self, json: Optional[dict[str, Any]] = None
    ) -> "Generator[AccountGroupItem, None, None]":
        if json is None:
            json = {}

        mindbridgequeryterm = MindBridgeQueryTerm.model_validate(json)
        json_str = mindbridgequeryterm.model_dump_json(
            by_alias=True, exclude_none=True, warnings=False
        )
        logger.info(f"Query (get) is: {json_str}")

        if "accountGroupingId" not in json_str:
            raise ParameterError(
                parameter_name="json",
                details=(
                    "At least one valid accountGroupingId term must be provided when "
                    "querying this entity."
                ),
            )

        url = f"{self.base_url}/query"
        for resp_dict in super()._get(url=url, json=json):
            yield AccountGroupItem.model_validate(resp_dict)

    def update(self, account_group: AccountGroupItem) -> AccountGroupItem:
        if getattr(account_group, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{account_group.id}"
        resp_dict = super()._update(url=url, json=account_group.update_json)

        return AccountGroupItem.model_validate(resp_dict)
