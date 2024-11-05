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
import warnings
from mindbridgeapi.async_result_item import AsyncResultItem, AsyncResultType
from mindbridgeapi.async_results import AsyncResults
from mindbridgeapi.base_set import BaseSet
from mindbridgeapi.exceptions import ItemError, ItemNotFoundError, ParameterError
from mindbridgeapi.generated_pydantic_model.model import (
    ApiDataTableExportRequest,
    ApiDataTableQuerySortOrder,
    ApiDataTableRead,
    Direction,
    MindBridgeQueryTerm,
)
from mindbridgeapi.generated_pydantic_model.model import Type4 as DataTableColumnType

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class DataTables(BaseSet):
    def __post_init__(self) -> None:
        self.async_result_set = AsyncResults(server=self.server)

    @cached_property
    def base_url(self) -> str:
        return f"{self.server.base_url}/data-tables"

    def get_by_id(self, id: str) -> ApiDataTableRead:
        url = f"{self.base_url}/{id}"
        resp_dict = super()._get_by_id(url=url)

        return ApiDataTableRead.model_validate(resp_dict)

    def get(
        self, json: Optional[dict[str, Any]] = None
    ) -> "Generator[ApiDataTableRead, None, None]":
        logger.info("Starting Query (get)")

        if json is None:
            json = {}

        mindbridgequeryterm = MindBridgeQueryTerm.model_validate(json)
        json_str = mindbridgequeryterm.model_dump_json(
            by_alias=True, exclude_none=True, warnings=False
        )
        logger.info(f"Query (get) is: {json_str}")

        if "analysisId" not in json_str:
            raise ParameterError(
                parameter_name="json",
                details=(
                    "At least one valid analysisId term must be provided when querying "
                    "this entity."
                ),
            )

        url = f"{self.base_url}/query"
        for resp_dict in super()._get(url=url, json=json):
            yield ApiDataTableRead.model_validate(resp_dict)

    @staticmethod
    def _export_get_fields(
        input_item: ApiDataTableRead, fields: Optional[list[str]] = None
    ) -> list[str]:
        if fields:
            return fields

        if input_item.columns is None:
            raise ItemError(f"{input_item.columns=}.")

        """
        "KEYWORD_SEARCH columns can't be included in data table exports. Attempting to
            select them as part of fields will cause the export request to fail.".
            Similarly fields that are filter only can't be included as fields.
        """
        return [
            x.field
            for x in input_item.columns
            if x.type != DataTableColumnType.KEYWORD_SEARCH
            and x.field is not None
            and not x.filter_only
        ]

    @staticmethod
    def _export_get_sort(
        input_item: ApiDataTableRead,
        sort_direction: Optional[Direction] = None,
        sort_field: Optional[str] = None,
    ) -> ApiDataTableQuerySortOrder:
        if sort_direction is None:
            sort_direction = Direction.ASC

        try:
            sort_direction = Direction(sort_direction)
        except ValueError as err:
            raise ParameterError(
                parameter_name="sort_direction", details="Not a valid Direction."
            ) from err

        if sort_field is not None and not isinstance(sort_field, str):
            raise ParameterError(
                parameter_name="sort_field", details="Not provided as str."
            )

        if sort_field is None and input_item.type == "flows_compact":
            sort_field = "flow_id"
        elif sort_field is None and input_item.logical_name == "gl_journal_lines":
            sort_field = "rowid"
        elif sort_field is None and input_item.logical_name == "gl_journal_tx":
            sort_field = "txid"
        elif sort_field is None or sort_field == "":
            # Don't send a sort
            sort_field = None
            sort_direction = None

        return ApiDataTableQuerySortOrder(direction=sort_direction, field=sort_field)

    def export(
        self,
        input_item: ApiDataTableRead,
        fields: Optional[list[str]] = None,
        query: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        sort_direction: Optional[Direction] = None,
        sort_field: Optional[str] = None,
    ) -> AsyncResultItem:
        if getattr(input_item, "id", None) is None:
            raise ItemNotFoundError

        fields = self._export_get_fields(input_item=input_item, fields=fields)

        if query is None:
            query = {}

        mindbridge_query_term = MindBridgeQueryTerm.model_validate(query)

        sort = self._export_get_sort(
            input_item=input_item, sort_direction=sort_direction, sort_field=sort_field
        )

        url = f"{self.base_url}/{input_item.id}/export"
        data_table_export_request = ApiDataTableExportRequest(
            fields=fields, query=mindbridge_query_term, limit=limit, sort=sort
        )

        json = data_table_export_request.model_dump(
            mode="json", by_alias=True, exclude_none=True
        )

        resp_dict = super()._create(url=url, json=json)

        return AsyncResultItem.model_validate(resp_dict)

    def wait_for_export(
        self,
        async_result: AsyncResultItem,
        check_interval_seconds: int = -873,  # Depreciated
        max_wait_minutes: int = (24 * 60),
    ) -> None:
        """Wait for the async result for the data table export to complete

        Waits, at most the minutes specified, for the async result to be COMPLETE and
        raises and error if any error

        Args:
            async_result (AsyncResultItem): Async result to check
            max_wait_minutes (int): Maximum minutes to wait (default: `24 * 60`)

        Raises:
            ValueError: If not a DATA_TABLE_EXPORT
        """
        if check_interval_seconds != -873:
            warnings.warn(
                "check_interval_seconds was provided to wait_for_export as "
                f"{check_interval_seconds}. This will not be referenced as now the "
                "check interval will be exponentially increasing to a max interval",
                category=DeprecationWarning,
                stacklevel=2,
            )

        del check_interval_seconds

        if async_result.type != AsyncResultType.DATA_TABLE_EXPORT:
            raise ItemError(f"{async_result.type=}.")

        self.async_result_set._wait_for_async_result(
            async_result=async_result,
            max_wait_minutes=max_wait_minutes,
            init_interval_sec=10,
        )

    def download(
        self, async_result: AsyncResultItem, output_file_path: "Path"
    ) -> "Path":
        if async_result.id is None:
            raise ItemNotFoundError

        async_result = self.server.async_results.get_by_id(async_result.id)

        file_result_id = async_result._get_file_result_id(
            expected_type=AsyncResultType.DATA_TABLE_EXPORT
        )

        file_result = self.server.file_results.get_by_id(file_result_id)

        return self.server.file_results.export(
            file_result=file_result, output_file_path=output_file_path
        )
