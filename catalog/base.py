import pandas as pd
from pathlib import Path
import json
import datetime


class CuratedData(object):

  def __init__(self,
               subject_id=None,
               hadm_id=None
               ):
    """Constructor for CuratedData"""
    if subject_id:
      self.subject_id = subject_id
    if hadm_id:
      self.hadm_id = hadm_id
    self.result = pd.DataFrame()
    self.d_result = None

  def set_subject_id(self, subject_id):
    self.subject_id = subject_id
    return self

  def set_hadm_id(self, hadm_id):
    self.hadm_id = hadm_id
    return self

  def toDF(self):
    return self.result

  def query(self):
    return self

  def preprocess(self):
    return self

  def export(self):
    return dict(columns=[], values=[])

  def to_json(self):
    if self.d_result:
      return dict(result=self.d_result)
    else:
      return dict(result=self.result.to_dict(orient="record"))

  def save_json(self, json_file):
    if self.d_result is None:
      self.d_result = self.to_json()

    with Path("output", json_file).open("w") as outfile:
      json.dump(self.d_result, outfile, indent=2, default=self.__default)

  def __default(self, o):
    if isinstance(o, (datetime.date, datetime.datetime)):
      return o.isoformat()


class NoSubjectIdException():
  pass
