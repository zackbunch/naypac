import pytest
from nay.core.image import Image

class TestImage:
    def test_valid_init(self):
        image = Image(name="sonarqube:latest", tag="v1", entrypoint=["/start.sh"])
        assert image.name == "sonarqube:latest"
        assert image.tag == "v1"
        assert image.entrypoint == ["/start.sh"]

    def test_valid_init_with_default_values(self):
        image = Image(name="sonarqube:latest")
        assert image.name == "sonarqube:latest"
        assert image.tag is None
        assert image.entrypoint is None

    def test_with_tag(self):
        original_image = Image(name="sonarqube:latest")
        modified_image = original_image.with_tag("v2")
        assert modified_image.name == "sonarqube:latest"
        assert modified_image.tag == "v2"
        assert modified_image.entrypoint is None

    def test_with_entrypoint(self):
        original_image = Image(name="sonarqube:latest")
        modified_image = original_image.with_entrypoint("/entrypoint.sh", "arg1", "arg2")
        assert modified_image.name == "sonarqube:latest"
        assert modified_image.tag is None
        assert modified_image.entrypoint == ["/entrypoint.sh", "arg1", "arg2"]

    def test_render_with_tag_and_entrypoint(self):
        image = Image(name="sonarqube:latest", tag="v1", entrypoint=["/start.sh"])
        rendered = image.render()
        assert rendered == {"name": "sonarqube:latest:v1", "entrypoint": ["/start.sh"]}

    def test_render_with_default_values(self):
        image = Image(name="sonarqube:latest")
        rendered = image.render()
        assert rendered == {"name": "sonarqube:latest"}

    def test_equals(self):
        image1 = Image(name="sonarqube:latest", tag="v1", entrypoint=["/start.sh"])
        image2 = Image(name="sonarqube:latest", tag="v1", entrypoint=["/start.sh"])
        assert image1._equals(image2)

    def test_not_equals(self):
        image1 = Image(name="sonarqube:latest", tag="v1", entrypoint=["/start.sh"])
        image2 = Image(name="sonarqube:latest", tag="v2", entrypoint=["/start.sh"])
        assert not image1._equals(image2)

# Run the tests with pytest
if __name__ == "__main__":
    pytest.main()
