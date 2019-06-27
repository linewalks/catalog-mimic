from catalog.cardio.model.base import Base
from sqlalchemy import Column, String, Integer, DateTime, Numeric


class CardioAdministration(Base):
  __tablename__ = "cardio_administration"
  __table_args__ = {"schema": "analysis"}

  id = Column(Integer, primary_key=True)
  subject_id = Column(Integer)
  latest_admittime = Column(DateTime)
  urgent = Column(Integer)
  emergency = Column(Integer)
  elective = Column(Integer)
  newborn = Column(Integer)
  count_of_icustay = Column(Integer)
  period_of_icustay = Column(Numeric)

  def __init__(self,
               subject_id,
               latest_admittime,
               urgent,
               emergency,
               elective,
               newborn,
               count_of_icustay,
               period_of_icustay):
    self.subject_id = subject_id
    self.latest_admittime = latest_admittime
    self.urgent = urgent
    self.emergency = emergency
    self.elective = elective
    self.newborn = newborn
    self.count_of_icustay = count_of_icustay
    self.period_of_icustay = period_of_icustay


class CardioDemographic(Base):
  __tablename__ = "cardio_demographic"
  __table_args__ = {"schema": "analysis"}

  id = Column(Integer, primary_key=True)
  subject_id = Column(Integer)
  hadm_id = Column(Integer)
  admittime = Column(DateTime)
  dob = Column(DateTime)
  age = Column(Numeric)
  gender = Column(String)
  insurance = Column(String)
  language = Column(String)
  religion = Column(String)
  marital_status = Column(String)
  ethnicity = Column(String)

  def __init__(self,
               subject_id,
               hadm_id,
               admittime,
               dob,
               age,
               gender,
               insurance,
               language,
               religion,
               marital_status,
               ethnicity):
    self.subject_id = subject_id
    self.hadm_id = hadm_id
    self.admittime = admittime
    self.dob = dob
    self.age = age
    self.gender = gender
    self.insurance = insurance
    self.language = language
    self.religion = religion
    self.marital_status = marital_status
    self.ethnicity = ethnicity


class CardioLabevents(Base):
  __tablename__ = "cardio_labevents"
  __table_args__ = {"schema": "analysis"}

  id = Column(Integer, primary_key=True)
  subject_id = Column(Integer)
  hadm_id = Column(Integer)
  itemid = Column(Integer)
  label = Column(String)
  fluid = Column(String)
  category = Column(String)
  loinc_code = Column(String)
  charttime = Column(DateTime)
  valuenum = Column(Numeric)
  valueuom = Column(String)

  def __init__(self,
               subject_id,
               hadm_id,
               itemid,
               label,
               fluid,
               category,
               loinc_code,
               charttime,
               valuenum,
               valueuom):
    self.subject_id = subject_id
    self.hadm_id = hadm_id
    self.itemid = itemid
    self.label = label
    self.fluid = fluid
    self.category = category
    self.loinc_code = loinc_code
    self.charttime = charttime
    self.valuenum = valuenum
    self.valueuom = valueuom


class CardioPrescription(Base):
  __tablename__ = "cardio_prescription"
  __table_args__ = {"schema": "analysis"}

  row_id = Column(Integer, primary_key=True)
  subject_id = Column(Integer)
  hadm_id = Column(Integer)
  icustay_id = Column(Integer)
  latest_date = Column(DateTime)
  drug = Column(String)
  drug_group = Column(String)
  prod_strength = Column(String)
  dose_val_rx = Column(String)
  dose_unit_rx = Column(String)
  form_val_disp = Column(String)
  form_unit_disp = Column(String)
  prescription_days = Column(Integer)

  def __init__(self,
               row_id,
               subject_id,
               hadm_id,
               icustay_id,
               latest_date,
               drug,
               drug_group,
               prod_strength,
               dose_val_rx,
               dose_unit_rx,
               form_val_disp,
               form_unit_disp,
               prescription_days):
    self.subject_id = subject_id
    self.hadm_id = hadm_id
    self.icustay_id = icustay_id
    self.latest_date = latest_date
    self.drug = drug
    self.drug_group = drug_group
    self.prod_strength = prod_strength
    self.dose_val_rx = dose_val_rx
    self.dose_unit_rx = dose_unit_rx
    self.form_val_disp = form_val_disp
    self.form_unit_disp = form_unit_disp
    self.prescription_days = prescription_days


class CardioProcedures(Base):
  __tablename__ = "cardio_procedures"
  __table_args__ = {"schema": "analysis"}

  id = Column(Integer, primary_key=True)
  subject_id = Column(Integer)
  hadm_id = Column(Integer)
  charttime = Column(DateTime)
  procedures = Column(String)
  icd9_code = Column(Integer)

  def __init__(self,
               subject_id,
               hadm_id,
               charttime,
               procedures,
               icd9_code):
    self.subject_id = subject_id
    self.hadm_id = hadm_id
    self.charttime = charttime
    self.procedures = procedures
    self.icd9_code = icd9_code


class CardioComorbidity(Base):
  __tablename__ = "cardio_comorbidity"
  __table_args__ = {"schema": "analysis"}

  id = Column(Integer, primary_key=True)
  subject_id = Column(Integer)
  hadm_id = Column(Integer)
  admittime = Column(DateTime)
  congestive_heart_failure = Column(Integer)
  cardiac_arrhythmias = Column(Integer)
  valvular_disease = Column(Integer)
  pulmonary_circulation = Column(Integer)
  peripheral_vascular = Column(Integer)
  hypertension = Column(Integer)
  paralysis = Column(Integer)
  other_neurological = Column(Integer)
  chronic_pulmonary = Column(Integer)
  hyperlipidemia = Column(Integer)
  diabetes_uncomplicated = Column(Integer)
  diabetes_complicated = Column(Integer)
  hypothyroidism = Column(Integer)
  renal_failure = Column(Integer)
  liver_disease = Column(Integer)
  peptic_ulcer = Column(Integer)
  aids = Column(Integer)
  lymphoma = Column(Integer)
  metastatic_cancer = Column(Integer)
  solid_tumor = Column(Integer)
  rheumatoid_arthritis = Column(Integer)
  coagulopathy = Column(Integer)
  obesity = Column(Integer)
  weight_loss = Column(Integer)
  fluid_electrolyte = Column(Integer)
  blood_loss_anemia = Column(Integer)
  deficiency_anemias = Column(Integer)
  alcohol_abuse = Column(Integer)
  drug_abuse = Column(Integer)
  psychoses = Column(Integer)
  depression = Column(Integer)

  def __init__(self,
               subject_id,
               hadm_id,
               admittime,
               congestive_heart_failure,
               cardiac_arrhythmias,
               valvular_disease,
               pulmonary_circulation,
               peripheral_vascular,
               hypertension,
               paralysis,
               other_neurological,
               chronic_pulmonary,
               hyperlipidemia,
               diabetes_uncomplicated,
               diabetes_complicated,
               hypothyroidism,
               renal_failure,
               liver_disease,
               peptic_ulcer,
               aids,
               lymphoma,
               metastatic_cancer,
               solid_tumor,
               rheumatoid_arthritis,
               coagulopathy,
               obesity,
               weight_loss,
               fluid_electrolyte,
               blood_loss_anemia,
               deficiency_anemias,
               alcohol_abuse,
               drug_abuse,
               psychoses,
               depression):
    self.subject_id = subject_id
    self.hadm_id = hadm_id
    self.admittime = admittime
    self.congestive_heart_failure = congestive_heart_failure
    self.cardiac_arrhythmias = cardiac_arrhythmias
    self.valvular_disease = valvular_disease
    self.pulmonary_circulation = pulmonary_circulation
    self.peripheral_vascular = peripheral_vascular
    self.hypertension = hypertension
    self.paralysis = paralysis
    self.other_neurological = other_neurological
    self.chronic_pulmonary = chronic_pulmonary
    self.hyperlipidemia = hyperlipidemia
    self.diabetes_uncomplicated = diabetes_uncomplicated
    self.diabetes_complicated = diabetes_complicated
    self.hypothyroidism = hypothyroidism
    self.renal_failure = renal_failure
    self.liver_disease = liver_disease
    self.peptic_ulcer = peptic_ulcer
    self.aids = aids
    self.lymphoma = lymphoma
    self.metastatic_cancer = metastatic_cancer
    self.solid_tumor = solid_tumor
    self.rheumatoid_arthritis = rheumatoid_arthritis
    self.coagulopathy = coagulopathy
    self.obesity = obesity
    self.weight_loss = weight_loss
    self.fluid_electrolyte = fluid_electrolyte
    self.blood_loss_anemia = blood_loss_anemia
    self.deficiency_anemias = deficiency_anemias
    self.alcohol_abuse = alcohol_abuse
    self.drug_abuse = drug_abuse
    self.psychoses = psychoses
    self.depression = depression
