#!/usr/bin/env python3

import unittest
from unittest.mock import patch

import pandas as pd

from src.best_record_company import best_record_company, main


def spy_decorator(method_to_decorate, name):
    """Wrap a bound method so calls are recorded without losing behavior.

    Copied from the assignment's former tmc.utils helper (originally from
    https://stackoverflow.com/questions/25608107) so the test suite no
    longer depends on the vendored tmc package.
    """
    from unittest.mock import MagicMock

    mock = MagicMock(name="%s method" % name)

    def wrapper(self, *args, **kwargs):
        mock(*args, **kwargs)
        return method_to_decorate(self, *args, **kwargs)

    wrapper.mock = mock
    return wrapper


class TestBestRecordCompany(unittest.TestCase):
    """best_record_company() -> chart rows for the top-charting publisher."""

    def test_shape(self):
        df = best_record_company()
        self.assertEqual(
            df.shape,
            (7, 7),
            msg="best_record_company() should return a DataFrame with "
            "shape (7, 7): the 7 chart rows belonging to the best "
            "publisher. Incorrect shape!",
        )

    def test_column_names(self):
        cols = ["Pos", "LW", "Title", "Artist", "Publisher", "Peak Pos", "WoC"]
        df = best_record_company()
        self.assertCountEqual(
            df.columns,
            cols,
            msg="best_record_company() should return a DataFrame with "
            "exactly these chart columns. Incorrect column names!",
        )

    def test_publisher(self):
        df = best_record_company()
        self.assertEqual(
            1,
            len(df["Publisher"].unique()),
            msg="The result should contain rows for a single publisher "
            "only -- the publisher should always be the same in the "
            "result!",
        )

    def test_calls(self):
        method = spy_decorator(pd.core.frame.DataFrame.groupby, "groupby")
        with patch(
            "src.best_record_company.best_record_company",
            wraps=best_record_company,
        ) as pbrc, patch.object(
            pd.core.frame.DataFrame, "groupby", new=method
        ), patch(
            "src.best_record_company.pd.read_csv", wraps=pd.read_csv
        ) as prc:
            main()
            pbrc.assert_called_once()
            prc.assert_called_once()
            method.mock.assert_called_once()
            args, kwargs = method.mock.call_args
            correct = (len(args) > 0 and args[0] == "Publisher") or (
                "by" in kwargs and kwargs["by"] == "Publisher"
            )
            self.assertTrue(
                correct,
                msg="Wrong or missing argument to groupby -- you should "
                "group by the 'Publisher' column!",
            )


if __name__ == "__main__":
    unittest.main()
