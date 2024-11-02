from datetime import datetime
from typing import ClassVar, Optional

from pydantic import HttpUrl, AnyHttpUrl

from ..node import OntolocyNode
from ..relationship import OntolocyRelationship
from .mitreattacktechnique import MitreAttackTechnique
from .control import Control


class MitreAttackMitigation(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "stix_id"
    __primarylabel__: ClassVar[str] = "MitreAttackMitigation"

    stix_id: str
    stix_type: str
    stix_created: datetime
    stix_modified: datetime
    stix_spec_version: str = "2.1"
    stix_revoked: Optional[bool] = False

    attack_spec_version: str
    attack_version: str
    attack_id: str
    attack_deprecated: Optional[bool] = False

    ref_url: HttpUrl
    name: str
    description: str


#
# OUTGOING RELATIONSHIPS
#


class MitreAttackMitigationDefendsAgainstTechnique(OntolocyRelationship):
    source: MitreAttackMitigation
    target: MitreAttackTechnique

    __relationshiptype__: ClassVar[str] = (
        "MITRE_ATTACK_MITIGATION_DEFENDS_AGAINST_TECHNIQUE"
    )


class MitreAttackMitigationMapsToControl(OntolocyRelationship):
    source: MitreAttackMitigation
    target: Control

    context: Optional[str] = None
    url_reference: Optional[AnyHttpUrl] = None

    __relationshiptype__: ClassVar[str] = "MITRE_ATTACK_MITIGATION_MAPS_TO_CONTROL"
