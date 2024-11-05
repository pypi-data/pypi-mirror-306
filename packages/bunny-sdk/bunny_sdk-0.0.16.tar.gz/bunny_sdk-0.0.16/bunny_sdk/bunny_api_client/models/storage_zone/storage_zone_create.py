from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .edge_replication_regions import EdgeReplicationRegions
    from .standard_regions import StandardRegions

@dataclass
class StorageZoneCreate(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The Custom404FilePath property
    custom404_file_path: Optional[str] = None
    # The Name property
    name: Optional[str] = None
    # The OriginUrl property
    origin_url: Optional[str] = None
    # The Region property
    region: Optional[StandardRegions] = None
    # The ReplicationRegions property
    replication_regions: Optional[List[EdgeReplicationRegions]] = None
    # The Rewrite404To200 property
    rewrite404_to200: Optional[bool] = None
    # The ZoneTier property
    zone_tier: Optional[float] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> StorageZoneCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: StorageZoneCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return StorageZoneCreate()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .edge_replication_regions import EdgeReplicationRegions
        from .standard_regions import StandardRegions

        from .edge_replication_regions import EdgeReplicationRegions
        from .standard_regions import StandardRegions

        fields: Dict[str, Callable[[Any], None]] = {
            "Custom404FilePath": lambda n : setattr(self, 'custom404_file_path', n.get_str_value()),
            "Name": lambda n : setattr(self, 'name', n.get_str_value()),
            "OriginUrl": lambda n : setattr(self, 'origin_url', n.get_str_value()),
            "Region": lambda n : setattr(self, 'region', n.get_enum_value(StandardRegions)),
            "ReplicationRegions": lambda n : setattr(self, 'replication_regions', n.get_collection_of_enum_values(EdgeReplicationRegions)),
            "Rewrite404To200": lambda n : setattr(self, 'rewrite404_to200', n.get_bool_value()),
            "ZoneTier": lambda n : setattr(self, 'zone_tier', n.get_float_value()),
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
        writer.write_str_value("Custom404FilePath", self.custom404_file_path)
        writer.write_str_value("Name", self.name)
        writer.write_str_value("OriginUrl", self.origin_url)
        writer.write_enum_value("Region", self.region)
        writer.write_collection_of_enum_values("ReplicationRegions", self.replication_regions)
        writer.write_bool_value("Rewrite404To200", self.rewrite404_to200)
        writer.write_float_value("ZoneTier", self.zone_tier)
        writer.write_additional_data_value(self.additional_data)
    

