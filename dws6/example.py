#!/usr/bin/env python3
"""
DWS6 Example - Demonstrates basic usage of the Digital Workspace 6.0 platform.

This example shows how to:
1. Create a new workspace
2. Configure it for cloud deployment
3. Enable features for sustainability applications
4. Start and manage the workspace
"""

from dws6 import DigitalWorkspace, __version__


def main():
    """Run the DWS6 example."""
    print("=" * 60)
    print(f"DWS6 Digital Workspace Example (v{__version__})")
    print("=" * 60)
    print()
    
    # Create a new workspace
    print("Creating a new Digital Workspace...")
    workspace = DigitalWorkspace(name="climate-monitoring-demo")
    print(f"✓ Workspace '{workspace.name}' created")
    print()
    
    # Configure the workspace
    print("Configuring workspace...")
    workspace.configure({
        "cloud_provider": "aws",
        "region": "us-east-1",
        "features": [
            "energy-monitoring",
            "ai-agents",
            "carbon-tracking"
        ]
    })
    print("✓ Workspace configured")
    print()
    
    # Display configuration
    status = workspace.get_status()
    print("Workspace Status:")
    print(f"  Name: {status['name']}")
    print(f"  Configured: {status['configured']}")
    print(f"  Cloud Provider: {status['config']['cloud_provider']}")
    print(f"  Region: {status['config']['region']}")
    print()
    
    # Start the workspace
    print("Starting workspace...")
    if workspace.start():
        print("✓ Workspace started successfully")
        print()
        
        # Show running status
        status = workspace.get_status()
        print("Active Features:")
        for feature in status['features']:
            print(f"  • {feature}")
        print()
        
        # Simulate some work
        print("Workspace is now running and ready for use.")
        print("In a real application, you would:")
        print("  • Monitor energy consumption")
        print("  • Track carbon emissions")
        print("  • Run AI agents for optimization")
        print("  • Integrate with foundation models")
        print()
        
        # Stop the workspace
        print("Stopping workspace...")
        if workspace.stop():
            print("✓ Workspace stopped successfully")
    
    print()
    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
