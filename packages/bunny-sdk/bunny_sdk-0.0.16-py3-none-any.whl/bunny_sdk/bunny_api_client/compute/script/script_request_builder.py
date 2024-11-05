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
    from ...models.compute.script import Script
    from ...models.compute.script_create import ScriptCreate
    from .item.script_item_request_builder import ScriptItemRequestBuilder
    from .script_get_response import ScriptGetResponse

class ScriptRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /compute/script
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ScriptRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/compute/script?page={page}&perPage={perPage}&search={search}{&includeLinkedPullZones}", path_parameters)
    
    def by_id(self,id: int) -> ScriptItemRequestBuilder:
        """
        Gets an item from the BunnyApiClient.compute.script.item collection
        param id: The ID of the script that will be returned
        Returns: ScriptItemRequestBuilder
        """
        if id is None:
            raise TypeError("id cannot be null.")
        from .item.script_item_request_builder import ScriptItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return ScriptItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[ScriptRequestBuilderGetQueryParameters]] = None) -> Optional[ScriptGetResponse]:
        """
        [ListComputeScripts API Docs](https://docs.bunny.net/reference/computeedgescriptpublic_index)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[ScriptGetResponse]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .script_get_response import ScriptGetResponse

        return await self.request_adapter.send_async(request_info, ScriptGetResponse, None)
    
    async def post(self,body: ScriptCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Script]:
        """
        [AddComputeScript API Docs](https://docs.bunny.net/reference/computeedgescriptpublic_addscript)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Script]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.compute.script import Script

        return await self.request_adapter.send_async(request_info, Script, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[ScriptRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        [ListComputeScripts API Docs](https://docs.bunny.net/reference/computeedgescriptpublic_index)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: ScriptCreate, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        [AddComputeScript API Docs](https://docs.bunny.net/reference/computeedgescriptpublic_addscript)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, '{+baseurl}/compute/script', self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> ScriptRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ScriptRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return ScriptRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class ScriptRequestBuilderGetQueryParameters():
        """
        [ListComputeScripts API Docs](https://docs.bunny.net/reference/computeedgescriptpublic_index)
        """
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "include_linked_pull_zones":
                return "includeLinkedPullZones"
            if original_name == "per_page":
                return "perPage"
            if original_name == "page":
                return "page"
            if original_name == "search":
                return "search"
            return original_name
        
        include_linked_pull_zones: Optional[bool] = None

        page: Optional[int] = None

        per_page: Optional[int] = None

        # The search term that will be used to filter the results
        search: Optional[str] = None

    
    @dataclass
    class ScriptRequestBuilderGetRequestConfiguration(RequestConfiguration[ScriptRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class ScriptRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

