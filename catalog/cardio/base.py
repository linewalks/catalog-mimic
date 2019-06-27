from catalog.base import CuratedData
from catalog.cardio.model.cardio_cohort import (CardioAdministration as cadm,
                                                CardioDemographic as cdemo,
                                                CardioProcedures as cproc,
                                                CardioLabevents as clab,
                                                CardioPrescription as cpres,
                                                CardioComorbidity as ccom)
from catalog.cardio.model.base import Session
from sqlalchemy import func, and_, case

session = Session()


class PatientDemographic(CuratedData):
  """인구통계 카탈로그 클래스(심혈관질환자의 최초 입원 시점 기준으로 추출)"""

  def __init__(self):
    super(PatientDemographic, self).__init__()

  def query(self):
    age_tbl = session.query(cdemo.subject_id,
                            func.min(cdemo.age).label("age")).group_by(cdemo.subject_id).cte("age_tbl")
    self.query = session.query(cdemo.subject_id,
                               cdemo.hadm_id, cdemo.dob, cdemo.age, cdemo.gender,
                               cdemo.insurance, cdemo.language,
                               cdemo.religion, cdemo.marital_status, cdemo.ethnicity
                               ).join(age_tbl,
                                      and_(cdemo.subject_id == age_tbl.c.subject_id,
                                           cdemo.age == age_tbl.c.age))

    return self

  def export(self):
    r = []
    for row in self.query:
      r.append(row._asdict())
    return r


class PatientAdministration(CuratedData):
  """입원패턴 카탈로그 클래스"""

  def __init__(self):
    super(PatientAdministration, self).__init__()

  def query(self):
    self.query = session.query(cadm.subject_id,
                               cadm.latest_admittime,
                               cadm.urgent,
                               cadm.emergency,
                               cadm.elective,
                               cadm.newborn,
                               cadm.count_of_icustay,
                               cadm.period_of_icustay).all()
    return self

  def export(self):
    r = []
    for row in self.query:
      r.append(row._asdict())
    return r


class PatientLabEvents(CuratedData):
  """검사결과 카탈로그 클래스"""

  def __init__(self):
    super(PatientLabEvents).__init__()

  def query(self):
    self.query = session.query(clab.subject_id,
                               clab.hadm_id,
                               clab.itemid,
                               clab.label,
                               clab.fluid,
                               clab.category,
                               clab.loinc_code,
                               clab.charttime,
                               clab.valuenum,
                               clab.valueuom).all()
    return self

  def export(self):
    r = []
    for row in self.query:
      r.append(row._asdict())
    return r


class PatientPrescription(CuratedData):
  """투약이력 카탈로그 클래스"""

  def __init__(self):
    super(PatientPrescription).__init__()

  def query(self):
    self.query = session.query(cpres.row_id,
                               cpres.subject_id,
                               cpres.hadm_id,
                               cpres.icustay_id,
                               cpres.latest_date,
                               cpres.drug,
                               cpres.drug_group,
                               cpres.prod_strength,
                               cpres.dose_val_rx,
                               cpres.dose_unit_rx,
                               cpres.form_val_disp,
                               cpres.form_unit_disp,
                               cpres.prescription_days).all()
    return self

  def export(self):
    r = []
    for row in self.query:
      r.append(row._asdict())
    return r


class PatientProcedure(CuratedData):
  """의료행위 카탈로그 클래스"""

  def __init__(self):
    super(PatientProcedure).__init__()

  def query(self):
    procedure_mask = case(
        [
            (cproc.icd9_code.in_(("3610", "3611", "3612", "3613", "3614", "3615",
                                  "3616", "3617")), "CABG"),
            (cproc.icd9_code.in_(("3631", "3632", "3633", "3634")), "TMR"),
            (cproc.icd9_code.in_(("8951", "8952", "8953", "8955", "8850", "8851",
                                  "8852", "8853", "8854", "8957")), "ECG"),
            (cproc.icd9_code.in_(("8941", "8943", "8944")), "STRESS"),
            (cproc.icd9_code.in_(("9205")), "SPECT"),
            (cproc.icd9_code.in_(("9336")), "REHAB"),
            (cproc.icd9_code.in_(("8855", "8856", "8857")), "CAG"),
            (cproc.icd9_code.in_(("3606", "3607")), "PCI"),
            (cproc.icd9_code.in_(("8872", "8877")), "ULTRASOUND"),
            (cproc.icd9_code.in_(("3728")), "ECHO")
        ],
        else_="OTHERS").label("sub_category")

    self.query = session.query(cproc.subject_id,
                               cproc.hadm_id,
                               cproc.charttime,
                               cproc.procedures,
                               procedure_mask,
                               cproc.icd9_code
                               ).all()
    return self

  def export(self):
    r = []
    for row in self.query:
      r.append(row._asdict())
    return r


class PatientComorbidity(CuratedData):
  """의료행위 카탈로그 클래스"""

  def __init__(self):
    super(PatientComorbidity).__init__()

  def query(self):
    self.query = session.query(ccom.subject_id,
                               ccom.hadm_id,
                               ccom.admittime,
                               ccom.congestive_heart_failure,
                               ccom.cardiac_arrhythmias,
                               ccom.valvular_disease,
                               ccom.pulmonary_circulation,
                               ccom.peripheral_vascular,
                               ccom.hypertension,
                               ccom.paralysis,
                               ccom.other_neurological,
                               ccom.chronic_pulmonary,
                               ccom.hyperlipidemia,
                               ccom.diabetes_uncomplicated,
                               ccom.diabetes_complicated,
                               ccom.hypothyroidism,
                               ccom.renal_failure,
                               ccom.liver_disease,
                               ccom.peptic_ulcer,
                               ccom.aids,
                               ccom.lymphoma,
                               ccom.metastatic_cancer,
                               ccom.solid_tumor,
                               ccom.rheumatoid_arthritis,
                               ccom.coagulopathy,
                               ccom.obesity,
                               ccom.weight_loss,
                               ccom.fluid_electrolyte,
                               ccom.blood_loss_anemia,
                               ccom.deficiency_anemias,
                               ccom.alcohol_abuse,
                               ccom.drug_abuse,
                               ccom.psychoses,
                               ccom.depression
                               ).all()
    return self

  def export(self):
    r = []
    for row in self.query:
      r.append(row._asdict())
    return r
