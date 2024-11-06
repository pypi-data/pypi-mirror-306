from opentrons.protocols.models.json_protocol import Labware


class LabwareWrapper:
    def __init__(self, labware: Labware, position: str) -> None:
        self.labware = labware
        self.position = position
