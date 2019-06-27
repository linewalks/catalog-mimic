
import pytest
from pathlib import Path
from catalog.cardio.pattern import (DiagnosisSankey,
                                    AdmissionByDiagnosisSankey,
                                    PrescriptionByDiagnosisSankey,
                                    LabByDiagnosisSankey,
                                    ProcedureByDiagnosisSankey,
                                    EventFlow,
                                    ClinicalTimeline,
                                    AdmissionSankey,
                                    LabSankey,
                                    PrescriptionSankey)


@pytest.mark.cardio_event_pattern
class Test_cardio_event_pattern():
  """Sample Test
  $ pytest -m cardio_event_pattern -s tests/
  """
  @pytest.fixture
  def from_to_event(self):
    return ("ischemic_hd", "congestive_hf")

  def test_diagnosis(self, from_to_event):
    from_event, to_event = from_to_event
    test = DiagnosisSankey(from_event, to_event).query().preprocess().export()
    assert len(test) > 0

  def test_administration(self, from_to_event):
    from_event, to_event = from_to_event
    test = AdmissionByDiagnosisSankey(from_event, to_event).query().export()
    assert len(test) > 0

  def test_prescription(self, from_to_event):
    from_event, to_event = from_to_event
    test = PrescriptionByDiagnosisSankey(from_event, to_event).query().export()
    assert len(test) > 0

  def test_lab(self, from_to_event):
    from_event, to_event = from_to_event
    test = LabByDiagnosisSankey(from_event, to_event).query().export()
    assert len(test) > 0

  def test_procedure(self, from_to_event):
    from_event, to_event = from_to_event
    test = ProcedureByDiagnosisSankey(from_event, to_event).query().export()
    assert len(test) > 0


@pytest.mark.cardio_event_seq
class Test_cardio_event_seq():
  """Cardio Event Sequence Test
  $ pytest -m cardio_event_seq -s tests/
  """

  def test_eventflow(self):
    test = EventFlow(n=10, min_evt_num=4).query().preprocess()
    json_file = "test_ev.json"
    test.save_json(json_file)
    test_file = Path("output", json_file)
    assert test_file.exists()
    test_file.unlink()

  def test_clinicaltimeline(self):
    test = ClinicalTimeline(subject_id=18803).query().preprocess()
    json_file = "test_ct.json"
    test.save_json(json_file)
    test_file = Path("output", json_file)
    assert test_file.exists()
    test_file.unlink()

  def test_admit_sankey(self):
    test = AdmissionSankey().query()
    json_file = "test_ska.json"
    test.save_json(json_file)
    test_file = Path("output", json_file)
    assert test_file.exists()
    test_file.unlink()

  def test_diagnosis_sankey(self):
    test = DiagnosisSankey().query()
    json_file = "test_skd.json"
    test.save_json(json_file)
    test_file = Path("output", json_file)
    assert test_file.exists()
    test_file.unlink()

  def test_lab_sankey(self):
    test = LabSankey().query()
    json_file = "test_skl.json"
    test.save_json(json_file)
    test_file = Path("output", json_file)
    assert test_file.exists()
    test_file.unlink()

  def test_prescription_sankey(self):
    test = PrescriptionSankey().query()
    json_file = "test_skp.json"
    test.save_json(json_file)
    test_file = Path("output", json_file)
    assert test_file.exists()
    test_file.unlink()
