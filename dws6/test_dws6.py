"""
Test suite for DWS6 Digital Workspace module.
"""

import unittest
from dws6 import (
    DigitalWorkspace,
    WorkspaceConfig,
    CloudProvider,
    FeatureType,
    __version__
)


class TestDigitalWorkspace(unittest.TestCase):
    """Test cases for the DigitalWorkspace class."""

    def test_version(self):
        """Test that version is defined."""
        self.assertIsNotNone(__version__)
        self.assertIsInstance(__version__, str)

    def test_workspace_initialization(self):
        """Test workspace can be initialized with a name."""
        workspace = DigitalWorkspace(name="test-workspace")
        self.assertEqual(workspace.name, "test-workspace")
        self.assertIsNone(workspace.config)
        self.assertFalse(workspace.is_running)

    def test_workspace_configuration(self):
        """Test workspace configuration."""
        workspace = DigitalWorkspace(name="test-workspace")
        
        config = {
            "cloud_provider": "aws",
            "region": "us-west-2",
            "features": ["energy-monitoring", "ai-agents"]
        }
        
        workspace.configure(config)
        
        self.assertIsNotNone(workspace.config)
        self.assertEqual(workspace.config.name, "test-workspace")
        self.assertEqual(workspace.config.cloud_provider, CloudProvider.AWS)
        self.assertEqual(workspace.config.region, "us-west-2")
        self.assertEqual(len(workspace.config.features), 2)

    def test_workspace_start_stop(self):
        """Test workspace can be started and stopped."""
        workspace = DigitalWorkspace(name="test-workspace")
        
        workspace.configure({
            "cloud_provider": "azure",
            "features": ["energy-monitoring"]
        })
        
        # Test start
        result = workspace.start()
        self.assertTrue(result)
        self.assertTrue(workspace.is_running)
        
        # Test stop
        result = workspace.stop()
        self.assertTrue(result)
        self.assertFalse(workspace.is_running)

    def test_workspace_start_without_config(self):
        """Test that starting workspace without config raises error."""
        workspace = DigitalWorkspace(name="test-workspace")
        
        with self.assertRaises(ValueError):
            workspace.start()

    def test_workspace_get_status(self):
        """Test getting workspace status."""
        workspace = DigitalWorkspace(name="test-workspace")
        
        # Status before configuration
        status = workspace.get_status()
        self.assertEqual(status["name"], "test-workspace")
        self.assertFalse(status["running"])
        self.assertFalse(status["configured"])
        
        # Status after configuration
        workspace.configure({
            "cloud_provider": "gcp",
            "features": ["hydrogen-planning"]
        })
        
        status = workspace.get_status()
        self.assertTrue(status["configured"])
        self.assertEqual(status["config"]["cloud_provider"], "gcp")

    def test_cloud_provider_enum(self):
        """Test CloudProvider enum values."""
        self.assertEqual(CloudProvider.AWS.value, "aws")
        self.assertEqual(CloudProvider.AZURE.value, "azure")
        self.assertEqual(CloudProvider.GCP.value, "gcp")

    def test_feature_type_enum(self):
        """Test FeatureType enum values."""
        self.assertEqual(FeatureType.ENERGY_MONITORING.value, "energy-monitoring")
        self.assertEqual(FeatureType.AI_AGENTS.value, "ai-agents")
        self.assertEqual(FeatureType.HYDROGEN_PLANNING.value, "hydrogen-planning")
        self.assertEqual(FeatureType.CARBON_TRACKING.value, "carbon-tracking")

    def test_workspace_config_dataclass(self):
        """Test WorkspaceConfig dataclass."""
        config = WorkspaceConfig(
            name="test",
            cloud_provider=CloudProvider.AWS,
            region="eu-west-1",
            features=[FeatureType.ENERGY_MONITORING],
            custom_config={"key": "value"}
        )
        
        self.assertEqual(config.name, "test")
        self.assertEqual(config.cloud_provider, CloudProvider.AWS)
        self.assertEqual(config.region, "eu-west-1")
        self.assertEqual(len(config.features), 1)
        self.assertEqual(config.custom_config["key"], "value")

    def test_invalid_feature_handling(self):
        """Test that invalid features are handled gracefully."""
        workspace = DigitalWorkspace(name="test-workspace")
        
        # This should not raise an error, just print a warning
        workspace.configure({
            "cloud_provider": "aws",
            "features": ["invalid-feature", "energy-monitoring"]
        })
        
        # Should only have the valid feature
        self.assertEqual(len(workspace.config.features), 1)
        self.assertEqual(workspace.config.features[0], FeatureType.ENERGY_MONITORING)


class TestWorkspaceIntegration(unittest.TestCase):
    """Integration tests for complete workspace workflows."""

    def test_full_workspace_lifecycle(self):
        """Test a complete workspace lifecycle."""
        # Create workspace
        workspace = DigitalWorkspace(name="integration-test")
        
        # Configure
        workspace.configure({
            "cloud_provider": "aws",
            "region": "us-east-1",
            "features": ["energy-monitoring", "ai-agents", "hydrogen-planning"]
        })
        
        # Start
        self.assertTrue(workspace.start())
        self.assertTrue(workspace.is_running)
        
        # Check status
        status = workspace.get_status()
        self.assertEqual(status["name"], "integration-test")
        self.assertTrue(status["running"])
        self.assertEqual(len(status["features"]), 3)
        
        # Stop
        self.assertTrue(workspace.stop())
        self.assertFalse(workspace.is_running)
        
        # Verify features are cleaned up
        status = workspace.get_status()
        self.assertEqual(len(status["features"]), 0)


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
