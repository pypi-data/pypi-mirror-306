from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..models.stream_video_library.video_library import VideoLibrary

@dataclass
class VideolibraryGetResponse(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The CurrentPage property
    current_page: Optional[int] = None
    # The HasMoreItems property
    has_more_items: Optional[bool] = None
    # The Items property
    items: Optional[List[VideoLibrary]] = None
    # The TotalItems property
    total_items: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VideolibraryGetResponse:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VideolibraryGetResponse
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VideolibraryGetResponse()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from ..models.stream_video_library.video_library import VideoLibrary

        from ..models.stream_video_library.video_library import VideoLibrary

        fields: Dict[str, Callable[[Any], None]] = {
            "CurrentPage": lambda n : setattr(self, 'current_page', n.get_int_value()),
            "HasMoreItems": lambda n : setattr(self, 'has_more_items', n.get_bool_value()),
            "Items": lambda n : setattr(self, 'items', n.get_collection_of_object_values(VideoLibrary)),
            "TotalItems": lambda n : setattr(self, 'total_items', n.get_int_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_int_value("CurrentPage", self.current_page)
        writer.write_bool_value("HasMoreItems", self.has_more_items)
        writer.write_collection_of_object_values("Items", self.items)
        writer.write_int_value("TotalItems", self.total_items)
        writer.write_additional_data_value(self.additional_data)
    

