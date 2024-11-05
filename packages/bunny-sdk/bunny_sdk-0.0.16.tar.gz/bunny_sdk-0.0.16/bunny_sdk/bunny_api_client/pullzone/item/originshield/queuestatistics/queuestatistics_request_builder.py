from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from .queuestatistics_get_response import QueuestatisticsGetResponse

class QueuestatisticsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /pullzone/{-id}/originshield/queuestatistics
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new QueuestatisticsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/pullzone/{%2Did}/originshield/queuestatistics{?dateFrom,dateTo,hourly}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueuestatisticsRequestBuilderGetQueryParameters]] = None) -> Optional[QueuestatisticsGetResponse]:
        """
        [GetOriginShieldQueueStatistics API Docs](https://docs.bunny.net/reference/pullzonepublic_originshieldconcurrencystatistics)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[QueuestatisticsGetResponse]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .queuestatistics_get_response import QueuestatisticsGetResponse

        return await self.request_adapter.send_async(request_info, QueuestatisticsGetResponse, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueuestatisticsRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        [GetOriginShieldQueueStatistics API Docs](https://docs.bunny.net/reference/pullzonepublic_originshieldconcurrencystatistics)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> QueuestatisticsRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: QueuestatisticsRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return QueuestatisticsRequestBuilder(self.request_adapter, raw_url)
    
    import datetime

    @dataclass
    class QueuestatisticsRequestBuilderGetQueryParameters():
        import datetime

        """
        [GetOriginShieldQueueStatistics API Docs](https://docs.bunny.net/reference/pullzonepublic_originshieldconcurrencystatistics)
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "date_from":
                return "dateFrom"
            if original_name == "date_to":
                return "dateTo"
            if original_name == "hourly":
                return "hourly"
            return original_name
        
        # The start date of the statistics. If no value is passed, the last 30 days will be returned.
        date_from: Optional[datetime.datetime] = None

        # The end date of the statistics. If no value is passed, the last 30 days will be returned.
        date_to: Optional[datetime.datetime] = None

        # If true, the statistics data will be returned in hourly grouping.
        hourly: Optional[bool] = None

    
    @dataclass
    class QueuestatisticsRequestBuilderGetRequestConfiguration(RequestConfiguration[QueuestatisticsRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

