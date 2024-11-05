from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .edge_script_variable import EdgeScriptVariable
    from .integration import Integration
    from .linked_pull_zone import LinkedPullZone

@dataclass
class Script(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The CurrentReleaseId property
    current_release_id: Optional[int] = None
    # The DefaultHostname property
    default_hostname: Optional[str] = None
    # The Deleted property
    deleted: Optional[bool] = None
    # The DeploymentKey property
    deployment_key: Optional[str] = None
    # The EdgeScriptVariables property
    edge_script_variables: Optional[List[EdgeScriptVariable]] = None
    # The Id property
    id: Optional[int] = None
    # The Integration property
    integration: Optional[Integration] = None
    # The IntegrationId property
    integration_id: Optional[int] = None
    # The LastModified property
    last_modified: Optional[datetime.datetime] = None
    # The LinkedPullZones property
    linked_pull_zones: Optional[List[LinkedPullZone]] = None
    # The MonthlyCost property
    monthly_cost: Optional[float] = None
    # The MonthlyCpuTime property
    monthly_cpu_time: Optional[int] = None
    # The MonthlyRequestCount property
    monthly_request_count: Optional[int] = None
    # The Name property
    name: Optional[str] = None
    # The RepositoryId property
    repository_id: Optional[int] = None
    # The ScriptType property
    script_type: Optional[float] = None
    # The SystemHostname property
    system_hostname: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Script:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Script
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Script()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .edge_script_variable import EdgeScriptVariable
        from .integration import Integration
        from .linked_pull_zone import LinkedPullZone

        from .edge_script_variable import EdgeScriptVariable
        from .integration import Integration
        from .linked_pull_zone import LinkedPullZone

        fields: Dict[str, Callable[[Any], None]] = {
            "CurrentReleaseId": lambda n : setattr(self, 'current_release_id', n.get_int_value()),
            "DefaultHostname": lambda n : setattr(self, 'default_hostname', n.get_str_value()),
            "Deleted": lambda n : setattr(self, 'deleted', n.get_bool_value()),
            "DeploymentKey": lambda n : setattr(self, 'deployment_key', n.get_str_value()),
            "EdgeScriptVariables": lambda n : setattr(self, 'edge_script_variables', n.get_collection_of_object_values(EdgeScriptVariable)),
            "Id": lambda n : setattr(self, 'id', n.get_int_value()),
            "Integration": lambda n : setattr(self, 'integration', n.get_object_value(Integration)),
            "IntegrationId": lambda n : setattr(self, 'integration_id', n.get_int_value()),
            "LastModified": lambda n : setattr(self, 'last_modified', n.get_datetime_value()),
            "LinkedPullZones": lambda n : setattr(self, 'linked_pull_zones', n.get_collection_of_object_values(LinkedPullZone)),
            "MonthlyCost": lambda n : setattr(self, 'monthly_cost', n.get_float_value()),
            "MonthlyCpuTime": lambda n : setattr(self, 'monthly_cpu_time', n.get_int_value()),
            "MonthlyRequestCount": lambda n : setattr(self, 'monthly_request_count', n.get_int_value()),
            "Name": lambda n : setattr(self, 'name', n.get_str_value()),
            "RepositoryId": lambda n : setattr(self, 'repository_id', n.get_int_value()),
            "ScriptType": lambda n : setattr(self, 'script_type', n.get_float_value()),
            "SystemHostname": lambda n : setattr(self, 'system_hostname', n.get_str_value()),
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
        writer.write_object_value("Integration", self.integration)
        writer.write_str_value("Name", self.name)
        writer.write_float_value("ScriptType", self.script_type)
        writer.write_additional_data_value(self.additional_data)
    

