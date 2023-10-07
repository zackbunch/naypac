import pytest
from nay.core.need import Need
from nay.core.variables import PredefinedVariables

class TestNeed:
    def test_valid_init_job(self):
        need = Need(job="my_job")
        assert need._job == "my_job"
        assert need._project is None
        assert need._ref is None
        assert need._pipeline is None
        assert need._artifacts is True

    def test_valid_init_pipeline(self):
        need = Need(pipeline="my_pipeline")
        assert need._job is None
        assert need._project is None
        assert need._ref is None
        assert need._pipeline == "my_pipeline"
        assert need._artifacts is True

    def test_valid_init_all_params(self):
        need = Need(job="my_job", project="my_project", ref="main", artifacts=False)
        assert need._job == "my_job"
        assert need._project == "my_project"
        assert need._ref == "main"
        assert need._pipeline is None
        assert need._artifacts is False

    def test_invalid_init_missing_job_and_pipeline(self):
        with pytest.raises(ValueError):
            Need()

    def test_invalid_init_ref_without_project(self):
        with pytest.raises(ValueError):
            Need(ref="main")


    def test_invalid_init_pipeline_equals_own_pipeline(self):
        with pytest.raises(ValueError):
            Need(pipeline=PredefinedVariables.CI_PIPELINE_ID)

    def test_render_job(self):
        need = Need(job="my_job")
        rendered = need.render()
        assert rendered == {"job": "my_job", "artifacts": True}

    def test_render_pipeline(self):
        need = Need(pipeline="my_pipeline")
        rendered = need.render()
        assert rendered == {"pipeline": "my_pipeline"}

    def test_equals(self):
        need1 = Need(job="my_job", project="my_project", ref="main", artifacts=False)
        need2 = Need(job="my_job", project="my_project", ref="main", artifacts=False)
        assert need1._equals(need2)

    def test_not_equals(self):
        need1 = Need(job="my_job1", project="my_project", ref="main", artifacts=False)
        need2 = Need(job="my_job2", project="my_project", ref="main", artifacts=False)
        assert not need1._equals(need2)
