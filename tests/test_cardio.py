# -*- coding: utf-8 -*-
import pytest
from pathlib import Path
import sqlalchemy
from catalog.cardio import base


@pytest.mark.cardio_gen
class Test_cardio_gen():
  """Generate all tables from the scratch
  $ pytest -m cardio_gen -s tests/
  """
  @pytest.fixture
  def sql_dir(self):
    return "catalog/cardio/sql"

  @pytest.fixture
  def sql_list(self, sql_dir):
    p = Path(sql_dir)
    return list(p.glob("*.sql"))

  def execute(self, p, db):
    with db.engine.connect() as conn:
      with p.open() as f:
        if db.__class__.__name__ == "DBLocal":
          conn.execute("set search_path=analysis,mimiciii,public")
        if db.__class__.__name__ == "DBRemote":
          conn.execute("set search_path=analysis,mimiciii,public")
        escaped_sql = sqlalchemy.sql.text(f.read())
        conn.execute(escaped_sql)

  def test_sql_list(self, sql_list):
    assert len(sql_list) > 0

  @pytest.mark.run(order=1)
  def test_0_cardio_cohort(self, db, sql_dir):
    p = Path(sql_dir, "0_cardio_cohort.sql")
    self.execute(p, db)

  @pytest.mark.skip(reason="skip all events")
  def test_1_cardio_events_all(self, db, sql_dir):
    p = Path(sql_dir, "1_1_cardio_events_all.sql")
    self.execute(p, db)

  @pytest.mark.run(order=2)
  def test_1_cardio_events(self, db, sql_dir):
    p = Path(sql_dir, "1_2_cardio_events.sql")
    self.execute(p, db)

  @pytest.mark.run(order=3)
  def test_2_admit_events(self, db, sql_dir):
    p = Path(sql_dir, "2_admit_events.sql")
    self.execute(p, db)

  @pytest.mark.run(order=4)
  def test_2_diagnoses_events(self, db, sql_dir):
    p = Path(sql_dir, "2_diagnosis_events.sql")
    self.execute(p, db)

  @pytest.mark.run(order=5)
  def test_2_icu_events(self, db, sql_dir):
    p = Path(sql_dir, "2_icu_events.sql")
    self.execute(p, db)

  @pytest.mark.run(order=6)
  def test_2_lab_events(self, db, sql_dir):
    p = Path(sql_dir, "2_lab_events.sql")
    self.execute(p, db)

  @pytest.mark.run(order=7)
  def test_2_prescription_events(self, db, sql_dir):
    p = Path(sql_dir, "2_prescription_events.sql")
    self.execute(p, db)

  @pytest.mark.run(order=8)
  def test_2_procedure_events(self, db, sql_dir):
    p = Path(sql_dir, "2_procedure_events.sql")
    self.execute(p, db)

  @pytest.mark.run(order=9)
  def test_2_comorbidity_events(self, db, sql_dir):
    p = Path(sql_dir, "2_comorbidity_events.sql")
    self.execute(p, db)


@pytest.mark.cardio_base
class Test_cardio_base():
  """Sample Test
  $ pytest -m cardio_base -s tests/
  """

  def test_demographic(self):
    test = base.PatientDemographic().query().export()
    assert len(test) == 18411

  def test_administration(self):
    test = base.PatientAdministration().query().export()
    assert len(test) == 18401

  def test_lab(self):
    test = base.PatientLabEvents().query().export()
    assert len(test) == 6441439

  def test_prescription(self):
    test = base.PatientPrescription().query().export()
    assert len(test) == 99417

  def test_procedure(self):
    test = base.PatientProcedure().query().export()
    assert len(test) == 88369

  def test_comorbidity(self):
    test = base.PatientComorbidity().query().export()
    assert len(test) == 26564
