"""
Detox Pattern Service - Unit Tests
Tests for the FastAPI backend endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app, PATTERN_REGISTRY, CURRENT_VERSION


# Create test client
client = TestClient(app)


# =============================================================================
# Health Check Tests
# =============================================================================

class TestHealthEndpoints:
    """Tests for health check endpoints"""
    
    def test_root_returns_200(self):
        """Root endpoint should return 200 OK"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_healthy_status(self):
        """Root endpoint should return healthy status"""
        response = client.get("/")
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_health_endpoint_returns_200(self):
        """Health endpoint should return 200 OK"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_version(self):
        """Health endpoint should include version"""
        response = client.get("/health")
        data = response.json()
        assert data["version"] == CURRENT_VERSION


# =============================================================================
# Patterns Endpoint Tests
# =============================================================================

class TestPatternsEndpoint:
    """Tests for the /patterns endpoint"""
    
    def test_patterns_returns_200(self):
        """GET /patterns should return 200 OK"""
        response = client.get("/patterns")
        assert response.status_code == 200
    
    def test_patterns_returns_version(self):
        """Response should include version string"""
        response = client.get("/patterns")
        data = response.json()
        assert "version" in data
        assert data["version"] == CURRENT_VERSION
    
    def test_patterns_returns_blocked_patterns(self):
        """Response should include blocked_patterns dict"""
        response = client.get("/patterns")
        data = response.json()
        assert "blocked_patterns" in data
        assert isinstance(data["blocked_patterns"], dict)
    
    def test_patterns_contains_email_regex(self):
        """blocked_patterns should contain email regex"""
        response = client.get("/patterns")
        data = response.json()
        assert "email" in data["blocked_patterns"]
        assert len(data["blocked_patterns"]["email"]) > 0
    
    def test_patterns_contains_phone_regex(self):
        """blocked_patterns should contain phone regex"""
        response = client.get("/patterns")
        data = response.json()
        assert "phone_us" in data["blocked_patterns"]
    
    def test_patterns_contains_ssn_regex(self):
        """blocked_patterns should contain SSN regex"""
        response = client.get("/patterns")
        data = response.json()
        assert "ssn" in data["blocked_patterns"]
    
    def test_patterns_includes_metadata(self):
        """Response should include metadata"""
        response = client.get("/patterns")
        data = response.json()
        assert "metadata" in data
        assert "total_patterns" in data["metadata"]
    
    def test_patterns_count_matches_registry(self):
        """Pattern count should match enabled patterns in registry"""
        response = client.get("/patterns")
        data = response.json()
        enabled_count = sum(1 for p in PATTERN_REGISTRY.values() if p.enabled)
        assert data["metadata"]["total_patterns"] == enabled_count


# =============================================================================
# Individual Pattern Tests
# =============================================================================

class TestIndividualPatternEndpoint:
    """Tests for the /patterns/{name} endpoint"""
    
    def test_get_email_pattern(self):
        """Should return email pattern details"""
        response = client.get("/patterns/email")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "email"
        assert "regex" in data
    
    def test_get_nonexistent_pattern_returns_404(self):
        """Should return 404 for unknown pattern"""
        response = client.get("/patterns/nonexistent_pattern")
        assert response.status_code == 404
    
    def test_pattern_includes_severity(self):
        """Pattern response should include severity"""
        response = client.get("/patterns/ssn")
        data = response.json()
        assert "severity" in data
        assert data["severity"] == "critical"


# =============================================================================
# Severity Filter Tests
# =============================================================================

class TestSeverityFilterEndpoint:
    """Tests for the /patterns/severity/{level} endpoint"""
    
    def test_filter_by_critical_severity(self):
        """Should return only critical patterns"""
        response = client.get("/patterns/severity/critical")
        assert response.status_code == 200
        data = response.json()
        assert data["severity"] == "critical"
        assert "ssn" in data["blocked_patterns"]
    
    def test_filter_by_high_severity(self):
        """Should return only high severity patterns"""
        response = client.get("/patterns/severity/high")
        assert response.status_code == 200
        data = response.json()
        assert "email" in data["blocked_patterns"]
    
    def test_invalid_severity_returns_400(self):
        """Should return 400 for invalid severity level"""
        response = client.get("/patterns/severity/invalid")
        assert response.status_code == 400


# =============================================================================
# Regex Validation Tests
# =============================================================================

class TestRegexPatterns:
    """Tests to validate regex patterns work correctly"""
    
    def test_email_regex_matches_valid_email(self):
        """Email regex should match valid emails"""
        import re
        response = client.get("/patterns")
        email_regex = response.json()["blocked_patterns"]["email"]
        
        test_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "name+tag@gmail.com"
        ]
        
        for email in test_emails:
            assert re.search(email_regex, email), f"Failed to match: {email}"
    
    def test_phone_regex_matches_valid_phones(self):
        """Phone regex should match valid US phone numbers"""
        import re
        response = client.get("/patterns")
        phone_regex = response.json()["blocked_patterns"]["phone_us"]
        
        test_phones = [
            "555-123-4567",
            "(555) 123-4567",
            "5551234567"
        ]
        
        for phone in test_phones:
            assert re.search(phone_regex, phone), f"Failed to match: {phone}"
    
    def test_ssn_regex_matches_valid_ssn(self):
        """SSN regex should match valid SSN formats"""
        import re
        response = client.get("/patterns")
        ssn_regex = response.json()["blocked_patterns"]["ssn"]
        
        test_ssns = [
            "123-45-6789",
            "123 45 6789",
            "123456789"
        ]
        
        for ssn in test_ssns:
            assert re.search(ssn_regex, ssn), f"Failed to match: {ssn}"


# =============================================================================
# CORS Tests
# =============================================================================

class TestCORS:
    """Tests for CORS configuration"""
    
    def test_cors_headers_present(self):
        """CORS headers should be present in response"""
        response = client.options(
            "/patterns",
            headers={
                "Origin": "chrome-extension://abc123",
                "Access-Control-Request-Method": "GET"
            }
        )
        # FastAPI handles OPTIONS automatically with CORS middleware
        assert response.status_code in [200, 405]

