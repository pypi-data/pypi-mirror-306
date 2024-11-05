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
    from .o_embed_get_response import OEmbedGetResponse

class OEmbedRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /OEmbed
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new OEmbedRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/OEmbed?expires={expires}&url={url}{&maxHeight,maxWidth,token}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[OEmbedRequestBuilderGetQueryParameters]] = None) -> Optional[OEmbedGetResponse]:
        """
        [OEmbed API Docs](https://docs.bunny.net/reference/oembed_getoembed)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[OEmbedGetResponse]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .o_embed_get_response import OEmbedGetResponse

        return await self.request_adapter.send_async(request_info, OEmbedGetResponse, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[OEmbedRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        [OEmbed API Docs](https://docs.bunny.net/reference/oembed_getoembed)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> OEmbedRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: OEmbedRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return OEmbedRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class OEmbedRequestBuilderGetQueryParameters():
        """
        [OEmbed API Docs](https://docs.bunny.net/reference/oembed_getoembed)
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "max_height":
                return "maxHeight"
            if original_name == "max_width":
                return "maxWidth"
            if original_name == "expires":
                return "expires"
            if original_name == "token":
                return "token"
            if original_name == "url":
                return "url"
            return original_name
        
        expires: Optional[int] = None

        max_height: Optional[int] = None

        max_width: Optional[int] = None

        token: Optional[str] = None

        url: Optional[str] = None

    
    @dataclass
    class OEmbedRequestBuilderGetRequestConfiguration(RequestConfiguration[OEmbedRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

