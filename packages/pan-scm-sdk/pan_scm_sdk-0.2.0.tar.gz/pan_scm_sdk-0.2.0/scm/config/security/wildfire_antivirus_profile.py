# scm/config/security/wildfire_antivirus_profiles.py

from typing import List, Dict, Any, Optional
from scm.config import BaseObject
from scm.models.security.wildfire_antivirus_profiles import (
    WildfireAntivirusProfileCreateModel,
    WildfireAntivirusProfileResponseModel,
    WildfireAntivirusProfileUpdateModel,
)
from scm.exceptions import ValidationError


class WildfireAntivirusProfile(BaseObject):
    """
    Manages WildFire Antivirus Profiles in Palo Alto Networks' Strata Cloud Manager.

    This class provides methods to create, retrieve, update, delete, and list WildFire Antivirus Profiles
    using the Strata Cloud Manager API. It supports operations within folders, snippets,
    or devices, and allows filtering of profiles based on various criteria.

    Attributes:
        ENDPOINT (str): The API endpoint for WildFire Antivirus Profile operations.

    Errors:
        ValidationError: Raised when invalid container parameters are provided.

    Returns:
        WildfireAntivirusProfileResponseModel: For create, get, and update methods.
        List[WildfireAntivirusProfileResponseModel]: For the list method.
    """

    ENDPOINT = "/config/security/v1/wildfire-anti-virus-profiles"

    def __init__(self, api_client):
        super().__init__(api_client)

    def create(self, data: Dict[str, Any]) -> WildfireAntivirusProfileResponseModel:
        """
        Create a new WildFire Antivirus Profile.

        Args:
            data (Dict[str, Any]): The data for the new profile.

        Returns:
            WildfireAntivirusProfileResponseModel: The created profile.
        """
        profile = WildfireAntivirusProfileCreateModel(**data)
        payload = profile.model_dump(exclude_unset=True)
        response = self.api_client.post(self.ENDPOINT, json=payload)
        return WildfireAntivirusProfileResponseModel(**response)

    def get(self, object_id: str) -> WildfireAntivirusProfileResponseModel:
        """
        Retrieve a WildFire Antivirus Profile by its ID.

        Args:
            object_id (str): The ID of the profile to retrieve.

        Returns:
            WildfireAntivirusProfileResponseModel: The retrieved profile.
        """
        endpoint = f"{self.ENDPOINT}/{object_id}"
        response = self.api_client.get(endpoint)
        return WildfireAntivirusProfileResponseModel(**response)

    def update(
        self,
        data: Dict[str, Any],
    ) -> WildfireAntivirusProfileResponseModel:
        """
        Update an existing WildFire Antivirus Profile.

        Args:
            data (Dict[str, Any]): The updated data for the profile.

        Returns:
            WildfireAntivirusProfileResponseModel: The updated profile.
        """
        profile = WildfireAntivirusProfileUpdateModel(**data)
        payload = profile.model_dump(exclude_unset=True)
        endpoint = f"{self.ENDPOINT}/{data['id']}"
        response = self.api_client.put(endpoint, json=payload)
        return WildfireAntivirusProfileResponseModel(**response)

    def delete(self, object_id: str) -> None:
        """
        Delete a WildFire Antivirus Profile.

        Args:
            object_id (str): The ID of the profile to delete.

        Returns:
            None
        """
        endpoint = f"{self.ENDPOINT}/{object_id}"
        self.api_client.delete(endpoint)

    def list(
        self,
        folder: Optional[str] = None,
        snippet: Optional[str] = None,
        device: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        name: Optional[str] = None,
        **filters,
    ) -> List[WildfireAntivirusProfileResponseModel]:
        """
        List WildFire Antivirus Profiles.

        Args:
            folder (Optional[str]): The folder to filter profiles.
            snippet (Optional[str]): The snippet to filter profiles.
            device (Optional[str]): The device to filter profiles.
            offset (Optional[int]): The pagination offset.
            limit (Optional[int]): The pagination limit.
            name (Optional[str]): Filter profiles by name.
            **filters: Additional filters.

        Returns:
            List[WildfireAntivirusProfileResponseModel]: The list of profiles.
        """
        params = {}
        error_messages = []

        # Validate offset and limit
        if offset is not None:
            if not isinstance(offset, int) or offset < 0:
                error_messages.append("Offset must be a non-negative integer")
        if limit is not None:
            if not isinstance(limit, int) or limit <= 0:
                error_messages.append("Limit must be a positive integer")

        # If there are any validation errors, raise ValueError with all error messages
        if error_messages:
            raise ValueError(". ".join(error_messages))

        # Include container type parameter
        container_params = {
            "folder": folder,
            "snippet": snippet,
            "device": device,
        }
        provided_containers = {
            k: v for k, v in container_params.items() if v is not None
        }

        if len(provided_containers) != 1:
            raise ValidationError(
                "Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        params.update(provided_containers)

        # Handle pagination parameters
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        # Handle filters
        if name is not None:
            params["name"] = name

        # Include any additional filters provided
        params.update(
            {
                k: v
                for k, v in filters.items()
                if v is not None
                and k not in container_params
                and k
                not in [
                    "offset",
                    "limit",
                    "name",
                ]
            }
        )

        response = self.api_client.get(self.ENDPOINT, params=params)
        profiles = [
            WildfireAntivirusProfileResponseModel(**item)
            for item in response.get("data", [])
        ]
        return profiles

    def fetch(
        self,
        name: str,
        folder: Optional[str] = None,
        snippet: Optional[str] = None,
        device: Optional[str] = None,
        **filters,
    ) -> Dict[str, Any]:
        """
        Fetches a single Wildfire Antivirus Profile object by name.

        Args:
            name (str): The name of the Wildfire Antivirus Profile to fetch.
            folder (str, optional): The folder in which the resource is defined.
            snippet (str, optional): The snippet in which the resource is defined.
            device (str, optional): The device in which the resource is defined.
            **filters: Additional filters to apply to the request.

        Returns:
            WildfireAntivirusProfileResponseModel: The fetched security rule object.

        Raises:
            ValidationError: If invalid parameters are provided.
            NotFoundError: If the security rule object is not found.
        """
        if not name:
            raise ValidationError("Parameter 'name' must be provided for fetch method.")

        params = {}

        # Include container type parameter
        container_params = {
            "folder": folder,
            "snippet": snippet,
            "device": device,
        }
        provided_containers = {
            k: v for k, v in container_params.items() if v is not None
        }

        if len(provided_containers) != 1:
            raise ValidationError(
                "Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        params.update(provided_containers)
        params["name"] = name  # Set the 'name' parameter

        # Include any additional filters provided
        params.update(
            {
                k: v
                for k, v in filters.items()
                if k
                not in [
                    "types",
                    "values",
                    "names",
                    "tags",
                    "folder",
                    "snippet",
                    "device",
                    "name",
                ]
            }
        )

        response = self.api_client.get(
            self.ENDPOINT,
            params=params,
        )

        # Since response is a single object when 'name' is provided
        # We can directly create the WildfireAntivirusProfileResponseModel
        profile = WildfireAntivirusProfileResponseModel(**response)
        return profile.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
