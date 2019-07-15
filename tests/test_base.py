# -*- coding: utf-8 -*-
import pytest
import json
import os
import pandas as pd
from catalog.base import CuratedData
from pathlib import Path


def json_of_response(response):
  """Decode json from response"""
  return json.loads(response.data.decode("utf8"))


def check_response_format(response):
  json_response = json_of_response(response)
  assert "result" in json_response.keys()


@pytest.mark.base
class Test_base():
  """Sample Test
  $ pytest -m base -s tests/
  """

  def test_func_1(self):
    a = CuratedData()
    assert a.toDF().shape[0] == 0

  @pytest.mark.xfail(raises=KeyError)
  def test_undefined_env(self):
    os.environ["FOO"]

  def test_env(self):
    assert os.environ["BAR"] == "bar"

  def test_save_json(self):
    test = CuratedData()
    json_file = "test.json"
    test.save_json(json_file)
    test_file = Path("output", json_file)
    assert test_file.exists()
    test_file.unlink()
