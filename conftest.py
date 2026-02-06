"""
Pytest configuration and fixtures for Detox Pattern Service tests.
"""

import pytest
import sys
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure async backend for pytest-asyncio"""
    return "asyncio"

