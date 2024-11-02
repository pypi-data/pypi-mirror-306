from http import HTTPMethod, HTTPStatus
from json import JSONDecodeError
from typing import Optional, IO, TypeVar
from urllib.parse import urlencode

from requests import HTTPError, Session

from automatic_contract_creation.scr.utils.omd_entities import (
    BaseModel,
    Table
)

from automatic_contract_creation.scr.utils.omd_helper import obj_to_json, model_to_field_names
from automatic_contract_creation.scr.utils.omd_exceptions import OpenmetadataException, OpenmetadataNotFound, OpenmetadataUnauthorized

T = TypeVar("T", bound=BaseModel)

class OMDClient:
    def __init__(
            self,
            *,
            base_url: str,
            token: str,
            timeout: Optional[float | tuple[float, float]] = None
    ):
        """
        :param base_url: OMD instance URL
        :param token: Permanent OMD token
        :param timeout: (optional) How long to wait for the server to send data before giving up,
            as a float, or a (connect timeout, read timeout) tuple
        """
        self._base_url = base_url
        self._timeout = timeout
        self._session = Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
            },
        )

    def _build_url(
            self,
            *,
            path: str,
            fields: Optional[str] = None,
            count: Optional[int] = None,
            **kwargs,
    ) -> str:
        query = urlencode(
            {
                key: str(value).lower() if isinstance(value, bool) else value
                for key, value in {
                "fields": fields,
                "limit": count,
                **kwargs,
            }.items()
                if value is not None
            },
            doseq=True,
        )
        return f"{self._base_url}/api{path}?{query}"

    def _send_request(
            self,
            *,
            method: HTTPMethod,
            url: str,
            data: Optional[BaseModel] = None,
            files: Optional[dict[str, IO]] = None,
    ) -> Optional[dict]:
        response = self._session.request(
            method=method,
            url=url,
            data=data and obj_to_json(data).encode(),
            files=files,
            headers=data and {"Content-Type": "application/json"},
            timeout=self._timeout,
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise OpenmetadataNotFound
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise OpenmetadataUnauthorized
        else:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise OpenmetadataException(
                    f"Unexpected status code for {method} {url}: {response.status_code}." +
                    f"{response.content}",
                ) from e

        # Avoid JSONDecodeError if status code was 2xx, but the response content is empty.
        # Some API endpoints return empty, non-JSON responses on success.
        if len(response.content) == 0:
            return

        try:
            return response.json()
        except JSONDecodeError as e:
            raise OpenmetadataException(
                f"Failed to decode response from {method} {url}, status={response.status_code}" +
                f"{response.content}",
            ) from e

    def _get(self, *, url: str) -> Optional[dict]:
        result = self._send_request(method=HTTPMethod.GET, url=url)
        return result



    def get_table(self, name: str) -> Table:
        return Table.model_validate(
            self._get(
                url=self._build_url(
                    path=f"/v1/tables/name/{name}",
                    fields=model_to_field_names(Table),
                ),
            ),
        )

