from typing import Dict, Any, Optional
from loki_logger import get_logger
from .api_service import APIService

class HubSpotAPIService:
    """
    Service for interacting with Hubspot fetch deals api
    """
    def __init__(self, base_url: str, test_delay_seconds: float = 0):
        self.api_service = APIService(
            base_url=base_url,
            test_delay_seconds=test_delay_seconds,
        )
        self.test_delay_seconds = test_delay_seconds
        self.logger = get_logger(__name__)

    # Authenticate HubSpot private app token
    def authenticate(self, access_token: str):
        self.logger.debug(
            "Validating access token",
            extra={'operation': 'authenticate'}
        )
        return self.api_service.validate_token(access_token=access_token)

    # HubSpot api call
    def get_deals(
        self,
        access_token: str,
        limit: int = 100,
        after: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        self.logger.debug(
            "Retrieving deals from HubSpot",
            extra={
                'operation': 'get_deals',
                'limit': limit,
                'has_cursor': after is not None,
                'test_delay_seconds': self.test_delay_seconds
            }
        )

        return self.api_service.get_data(
            access_token=access_token,
            limit=limit,
            after=after,
            **kwargs,
        )


        
