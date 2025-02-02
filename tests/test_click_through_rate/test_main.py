from pathlib import Path

import pytest

from click_through_rate.main import run_pipeline


class TestRunPipeline:
    @pytest.mark.slow
    @pytest.mark.integration
    def test_run_pipeline(self, path_settings: Path):
        run_pipeline(filepath=path_settings.resolve().as_posix())
