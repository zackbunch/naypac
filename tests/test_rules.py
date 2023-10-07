import pytest
from enum import Enum
from nay.core.rules import Rule, When

# Define a fixture for creating a default Rule instance
@pytest.fixture
def default_rule():
    return Rule()

# Define a fixture for creating a Klocwork Rule instance
@pytest.fixture
def klocwork_rule():
    return Rule(
        if_statement="KLOCWORK_ISSUES > 5",
        when=When.ON_FAILURE,
        allow_failure=True,
        variables={"KLOCWORK_ISSUES": "10", "KLOCWORK_SEVERITY": "high"},
    )

# Define test cases for the Rule class
class TestRule:
    def test_never(self, default_rule):
        new_rule = default_rule.never()
        assert new_rule._when == When.NEVER

    def test_add_variables(self, default_rule):
        default_rule.add_variables(KLOCWORK_ISSUES="10", KLOCWORK_SEVERITY="high")
        assert default_rule._variables == {"KLOCWORK_ISSUES": "10", "KLOCWORK_SEVERITY": "high"}

    def test_equals(self, klocwork_rule):
        # Create two Klocwork job rules with the same conditions
        rule1 = klocwork_rule
        rule2 = klocwork_rule
        assert rule1._equals(rule2)

    def test_not_equals(self, klocwork_rule):
        # Create two Klocwork job rules with different conditions
        rule1 = klocwork_rule
        rule2 = Rule(
            if_statement="KLOCWORK_ISSUES > 3",
            when=When.ON_FAILURE,
            allow_failure=True,
            variables={"KLOCWORK_ISSUES": "5", "KLOCWORK_SEVERITY": "medium"},
        )
        assert not rule1._equals(rule2)

    def test_render_klocwork_rule(self, klocwork_rule):
        # Render the Klocwork rule
        rendered_rule = klocwork_rule.render()

        # Define the expected rendering for a Klocwork job rule
        expected_rendering = {
            "if": "KLOCWORK_ISSUES > 5",
            "when": "on_failure",
            "allow_failure": True,
            "variables": {"KLOCWORK_ISSUES": "10", "KLOCWORK_SEVERITY": "high"},
        }

        # Assert that the rendered rule matches the expected rendering
        assert rendered_rule == expected_rendering

# Define test cases for the When enum
class TestWhen:
    def test_enum_values(self):
        assert When.ALWAYS.value == "always"
        assert When.DELAYED.value == "delayed"
        assert When.MANUAL.value == "manual"
        assert When.NEVER.value == "never"
        assert When.ON_FAILURE.value == "on_failure"
        assert When.ON_SUCCESS.value == "on_success"

# Run the tests with pytest
if __name__ == "__main__":
    pytest.main()
