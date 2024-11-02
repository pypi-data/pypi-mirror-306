"""
Author: Juha Meskanen
Date: 2024-10-26
"""

from typing import Any, Dict
import unittest
from unittest.mock import patch
from masterpiece.masterpiece import MasterPiece
from masterpiece.composite import Composite


class TestComposite(unittest.TestCase):
    """Unit tests for `Composite` class."""

    def setUp(self):
        """Set up test data for each test."""
        self.composite = Composite(name="group")
        self.child1 = MasterPiece(name="child1")
        self.child2 = MasterPiece(name="child2")

        self.root = Composite(
            "1",
            None,
            [
                Composite("2", None, [MasterPiece("4"), MasterPiece("5")]),
                Composite("3", None, [MasterPiece("6"), MasterPiece("7")]),
            ],
        )

    def test_composite_initialization(self):
        """Test initialization of the Composite object."""
        self.assertEqual(self.composite.name, "group")
        self.assertEqual(self.composite.role, "union")
        self.assertEqual(self.composite.children, [])

    def test_add_child(self):
        """Test adding a child to the composite."""
        self.composite.add(self.child1)
        self.assertIn(self.child1, self.composite.children)
        self.assertEqual(len(self.composite.children), 1)

        # Add another child
        self.composite.add(self.child2)
        self.assertIn(self.child2, self.composite.children)
        self.assertEqual(len(self.composite.children), 2)

    def test_to_dict(self):
        """Test serialization to a dictionary."""
        self.composite.add(self.child1)
        self.composite.add(self.child2)
        data = self.composite.to_dict()

        self.assertEqual(data["_class"], "Composite")
        self.assertEqual(data["_group"]["role"], "union")
        self.assertEqual(len(data["_group"]["children"]), 2)
        self.assertEqual(data["_group"]["children"][0]["_object"]["name"], "child1")
        self.assertEqual(data["_group"]["children"][1]["_object"]["name"], "child2")

    def test_from_dict(self):
        """Test deserialization from a dictionary."""
        data = {
            "_class": "Composite",
            "_object": {"name": "group", "payload": None},
            "_group": {
                "role": "union",
                "children": [
                    {
                        "_class": "MasterPiece",
                        "_object": {"name": "child1", "payload": None},
                    },
                    {
                        "_class": "MasterPiece",
                        "_object": {"name": "child2", "payload": None},
                    },
                ],
            },
        }

        self.composite.from_dict(data)
        self.assertEqual(self.composite.name, "group")
        self.assertEqual(self.composite.role, "union")
        self.assertEqual(len(self.composite.children), 2)
        self.assertEqual(self.composite.children[0].name, "child1")
        self.assertEqual(self.composite.children[1].name, "child2")

    @patch.object(MasterPiece, "run")
    def test_run_forever_and_shutdown(self, mock_run):
        """Test run_forever and shutdown behavior including children startup/shutdown."""
        self.composite.add(self.child1)
        self.composite.add(self.child2)

        # Test starting children
        with patch.object(self.composite, "info") as mock_info:
            self.composite.run_forever()
            self.assertEqual(mock_run.call_count, 2)
            mock_info.assert_any_call("Starting up 0 child1")
            mock_info.assert_any_call("Starting up 1 child2")
            mock_info.assert_any_call("All 2 children successfully started")

        # Test shutting down children
        with patch.object(self.composite, "info") as mock_info:
            self.composite.shutdown()
            mock_info.assert_any_call("Shutting down children")
            mock_info.assert_any_call("Shutting down thread 0 child1")
            mock_info.assert_any_call("Shutting down thread 1 child2")
            mock_info.assert_any_call("All 2 children successfully shut down")
            self.assertEqual(mock_info.call_count, 4)

    def test_traversal_visits_all_nodes(self):
        # A set to keep track of visited nodes
        visited_values = set()

        # Action that records each node's value
        def record_action(node: MasterPiece, context: Dict[str, Any]) -> bool:
            visited_values.add(node.name)
            return True  # Continue traversal

        # Run traversal
        self.root.do(record_action, {})

        # Assert that all nodes were visited
        self.assertEqual(visited_values, {"1", "2", "3", "4", "5", "6", "7"})

    def test_traversal_stops_on_false(self):
        # A set to keep track of visited nodes
        visited_values = set()

        # Action that stops traversal when value is 3
        def stop_action(node: MasterPiece, context: Dict[str, Any]) -> bool:
            visited_values.add(node.name)
            return node.name != "3"  # Stop if value is 3

        # Run traversal
        self.root.do(stop_action, {})

        # Assert that nodes beyond value 3 were not visited
        self.assertNotIn("6", visited_values)
        self.assertNotIn("7", visited_values)

    def test_context_passing(self):
        # Using context to filter which nodes to visit
        def context_sensitive_action(
            node: MasterPiece, context: Dict[str, Any]
        ) -> bool:
            stop_value = context.get("stop_value")
            return (
                node.name != stop_value
            )  # Stop traversal if node.name matches context stop_value

        # Test with stop_value "2"
        visited_values = set()
        self.root.do(
            lambda node, ctx: context_sensitive_action(node, ctx)
            and visited_values.add(node.name),
            {"stop_value": "2"},
        )

        # Assert that nodes with name "2" and its descendants were not visited
        self.assertNotIn("4", visited_values)
        self.assertNotIn("5", visited_values)
        self.assertNotIn("2", visited_values)

    def test_exception_handling(self):
        # Action that raises an exception for a specific node
        def exception_action(node: MasterPiece, context: Dict[str, Any]) -> bool:
            if node.name == "3":
                raise ValueError("Test exception")
            return True  # Continue traversal

        # Expect ValueError when calling do with the exception_action
        with self.assertRaises(ValueError):
            self.root.do(exception_action, {})


if __name__ == "__main__":
    unittest.main()
