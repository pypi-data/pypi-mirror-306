"""
Elementary class implementing hierarchy.

Author: Juha Meskanen
Date: 2024-10-26
"""

from typing import Callable, Any, Dict, List, Optional
from .masterpiece import MasterPiece


class Composite(MasterPiece):
    """Class implementing hierarchy. Objects of this class can consist of children.

    This class can be used for grouping masterpieces into larger entities to model
    any real world apparatus. Hierarchical entities can be manipulated exactly the
    same way as the most primitive objects, e.g. copied, serialized, or manipulated
    via do() method:

    Example:
    ::

        sensors = Composite("motionsensors")
        sensors.add(ShellyMotionSensor("downstairs"))
        sensors.add(ShellyMotionSensor("upstairs"))

        def some_action(node: MasterPiece, context : MyContext) -> bool:
            ...
            return 1 # continue traversal

        # Run traversal
        sensors.do(some_action, my_context)

    """

    def __init__(
        self,
        name: str = "group",
        payload: Optional[MasterPiece] = None,
        children: Optional[list[MasterPiece]] = None,
    ) -> None:
        super().__init__(name, payload)
        self.children: List[MasterPiece] = children or []
        self.role: str = "union"

    def add(self, h: MasterPiece) -> None:
        """Add new automation object as children. The object to be inserted
        must be derived from MasterPiece base class.

        Args:
            h (T): object to be inserted.
        """
        self.children.append(h)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["_group"] = {
            "role": self.role,
            "children": [child.to_dict() for child in self.children],
        }
        return data

    def from_dict(self, data: dict) -> None:
        """Recursively deserialize the group from a dictionary, including its
        children.

        Args:
            data (dict): data to deserialize from.
        """
        super().from_dict(data)
        for key, value in data.get("_group", {}).items():
            if key == "children":
                for child_dict in value:
                    child = MasterPiece.instantiate(child_dict["_class"])
                    self.add(child)
                    child.from_dict(child_dict)
            else:
                setattr(self, key, value)

    # @override
    def do(
        self,
        action: Callable[["MasterPiece", Dict[str, Any]], bool],
        context: Dict[str, Any],
    ) -> bool:
        """
        Recursively traverses the tree, from root to leaf, left to right direction,
        calling the provided `action` on each node.

        :param action: A callable that takes (node, context) and returns a boolean.
        :param context: Any context data that the action may use.
        :returns: None
        """
        if not super().do(action, context):
            return False
        for child in self.children:
            if not child.do(action, context):
                return False
        return True

    # @override
    def run_forever(self) -> None:
        """
        Dispatches first the call to all children and then to the super class.
        It is up to the sub classes to implement the actual functionality
        for this method.
        """

        self.start_children()
        super().run_forever()
        self.shutdown_children()

    def start_children(self) -> None:
        """Start  all children."""
        i: int = 0
        for s in self.children:
            self.info(f"Starting up {i} {s.name}")
            s.run()
            i = i + 1
        self.info(f"All {i} children successfully started")

    def shutdown_children(self) -> None:
        """Shuts down the children."""
        i: int = 0
        self.info("Shutting down children")
        for s in self.children:
            self.info(f"Shutting down thread {i} {s.name}")
            s.shutdown()
            i = i + 1
        self.info(f"All {i} children successfully shut down")

    # @override
    def shutdown(self) -> None:
        """Shuts down the object. First, it dispatches the call to all child objects,
        then calls the superclass method to stop the associated payload object, if one exists.
        """
        self.shutdown_children()
        super().shutdown()
