import pandas as pd

from catalog.base import (CuratedData,
                          NoSubjectIdException)

from catalog.cardio.model.cardio_events import CardioEvents as ce
from catalog.cardio.model.d_events import DEvents as de
from catalog.cardio.model.cardio_cohort import (CardioAdministration as cadm,
                                                CardioDemographic as cdemo,
                                                CardioProcedures as cproc,
                                                CardioLabevents as clab,
                                                CardioPrescription as cpres)
from catalog.cardio import Session
from sqlalchemy import func, case, and_, or_


session = Session()


class EventFlow(CuratedData):
  def __init__(self,
               n=10,
               min_evt_num=4):
    self.n = n
    self.min_evt_num = min_evt_num
    super(EventFlow, self).__init__()

  def query(self):
    query = session.\
        query(ce.subject_id,
              ce.ts,
              case([(de.event_name == "myocardial_inf, ischemic_hd", "myocardial_inf")],
                   else_=de.event_name).label("event_name")
              ).\
        distinct().\
        join(de, ce.event_id == de.event_id).\
        filter(de.category == "disease")
    self.result = pd.read_sql(query.statement, query.session.bind)
    return self

  def preprocess(self):
    if not set(["subject_id", "ts", "event_name"]).issubset(self.result.columns):
      self.result = self.result.iloc[0:0]
      return self.result

    ps = self.result.groupby("subject_id").size()
    sample_p = ps[ps > self.min_evt_num].sample(n=self.n).index
    self.result = self.result[self.result.subject_id.isin(sample_p)]
    self.result.rename(columns={"subject_id": "ENTITY_ID",
                                "ts": "TS",
                                "event_name": "EVENT_NAME"},
                       inplace=True)
    return self


class ClinicalTimeline(CuratedData):
  def __init__(self,
               subject_id):
    if subject_id is None:
      raise NoSubjectIdException
    super(ClinicalTimeline, self).__init__(subject_id=subject_id)

  def query(self):
    query = session.\
        query(ce.subject_id,
              ce.ts,
              de.category,
              de.event_name,
              ce.event_value
              ).\
        distinct().\
        join(de, ce.event_id == de.event_id).\
        filter(ce.subject_id == self.subject_id)
    self.result = pd.read_sql(query.statement, query.session.bind)
    return self

  def _tootlip_tables(self, x, header):
    return [[[header, x]]]

  def tootlip_depth(self, x, header):
    return [list(map(list, zip(header, x)))]

  def _map_drug_group(self, drug_list):
    d_drug_group = dict()
    grp_statin = [
        "atorvastatin", "pitavastatin", "lovastatin", "simvastatin",
        "pravastatin", "fluvastatin", "rosuvastatin"
    ]
    grp_p2y12_inh = [
        "clopidogrel", "ticlopidine", "ticagrelor", "prasugrel", "cangrelor"
    ]
    grp_nsaids = [
        "acetaminophen", "celecoxib", "diclofenac", "diflunisal",
        "etodolac", "ibuprofen", "indomethacin", "ketoprofen", "ketorolac",
        "nabumetone", "naproxen", "oxaprozin", "piroxicam", "salsalate",
        "sulindac", "tolmetin"
    ]
    grp_immunosuppr = [
        "tacrolimus", "cyclosporine", "mycophenolate mofetil",
        "mycophenolate sodium", "azathioprine", "sirolimus", "prednisone"
    ]
    grp_aspirin = ["aspirin"]

    for drug in drug_list:
      ldrug = drug.lower()
      if ldrug in (grp_statin):
        d_drug_group[drug] = "Statin"
      elif ldrug in (grp_immunosuppr):
        d_drug_group[drug] = "Immunosuppressant"
      elif ldrug in (grp_aspirin):
        d_drug_group[drug] = "Aspirin"
      elif ldrug in (grp_nsaids):
        d_drug_group[drug] = "NSAIDs"
      elif ldrug in (grp_p2y12_inh):
        d_drug_group[drug] = "P2Y12 inhibitor"
      else:
        d_drug_group[drug] = "Others"
    return d_drug_group

  def _make_absolute_times(self, label, df, ct_type="rect"):
    if df.shape[0] == 0:
      return []
    # adjust column names and type
    df.rename(columns={"ts": "starting_time"}, inplace=True)
    df["event_value"] = df.event_value.astype(float)

    if ct_type == "rect":
      df["ending_time"] = df.starting_time + pd.to_timedelta(df.event_value, unit="days")
    elif ct_type == "circle":
      df["ending_time"] = df.starting_time

    df["tooltip_tables"] = df.event_name.apply(self._tootlip_tables, header="event_name")

    return df[["starting_time", "ending_time", "tooltip_tables"]].to_dict(orient="record")

  def _make_relative_times(self, label, df, ct_type="rect"):
    if df.shape[0] == 0:
      return []
    # adjust column names and type
    df.rename(columns={"ts": "starting_time"}, inplace=True)
    df["event_value"] = pd.to_numeric(df.event_value, errors="coerce")
    df["event_value"] = df.event_value.dropna().astype(int)
    df_min_time = df.starting_time.min()

    df["starting_time"] = (df["starting_time"] - df_min_time).dt.days

    if ct_type == "rect":
      df["ending_time"] = df.starting_time + df.event_value
    elif ct_type == "circle":
      df["ending_time"] = df.starting_time

    df["display"] = ct_type

    df["tooltip_tables"] = df.event_name.apply(self._tootlip_tables, header="event_name")

    return df[["starting_time", "ending_time", "tooltip_tables", "display"]].to_dict(orient="record")

  def to_json(self):
    if not set(["subject_id", "ts", "event_name", "event_value"]).issubset(self.result.columns):
      self.result = self.result.iloc[0:0]
      return self.result

    ct_results = []
    for name, df in self.result.groupby("category"):
      ct_type = "rect"
      if name in ["procedure", "lab"]:
        ct_type = "circle"
      if name == "drug":
        d_drug_grp = self._map_drug_group(df.event_name.unique())
        df.event_name = df.event_name.map(d_drug_grp)
      d_result = dict(label=name,
                      times=self._make_relative_times(name, df.copy(), ct_type=ct_type),
                      visible=True,
                      display=ct_type)

      ct_results.append(d_result)

    self.d_result = ct_results
    return super(ClinicalTimeline, self).to_json()


class Sankey(CuratedData):
  def __init__(self):
    super(Sankey, self).__init__()

  def _node(self):
    # TODO:
    def tostr(x):
      return ",".join(map(str, x))

    self.result.from_event = self.result.from_event.apply(tostr)
    nodes = [{"name": i} for i in self.result.from_event.unique()]
    return nodes

  def _link(self):
    result = self.result
    result["to_event"] = result.groupby("subject_id")["from_ts"].shift(-1)
    result["to_ts"] = result.groupby("subject_id")["from_event"].shift(-1)
    result = result.dropna()
    result = result.groupby(["from_event", "to_event"]).size().to_frame(name="value").reset_index()

    result.columns = ["source", "target", "value"]
    return result.to_dict(orient="record")

  def to_json(self):
    result_json = dict()
    result_json["nodes"] = self._node()
    result_json["links"] = self._link()

    self.d_result = result_json

    return super(Sankey, self).to_json()


class AdmissionSankey(Sankey):
  def __init__(self):
    # TODO: might need filtering option
    super(AdmissionSankey, self).__init__()

  def query(self):
    # TODO:
    # string_agg(event_name, ', ' ORDER BY event_name) as from_event 변환
    tmp = session.\
        query(ce.subject_id,
              ce.ts,
              ce.event_id
              # case([(de.event_name == "myocardial_inf, ischemic_hd", "myocardial_inf")],
              #      else_=de.event_name).label("event_name")
              ).\
        distinct().\
        cte("tmp")

    query = session.\
        query(tmp.c.subject_id,
              tmp.c.ts.label("from_ts"),
              func.array_agg(tmp.c.event_id).label("from_event")
              # func.string_agg(de.event_name,
              #                 aggregate_order_by(literal_column(", "), de.event_name.desc())).label("from_event")
              ).\
        join(de, tmp.c.event_id == de.event_id).\
        filter(de.category == "admit").\
        group_by(tmp.c.subject_id, tmp.c.ts)
    self.result = pd.read_sql(query.statement, query.session.bind)
    return self

  def export(self):
    return super(AdmissionSankey, self).to_json()


class DiagnosisSankey(Sankey):

  def __init__(self,
               from_event=None,
               to_event=None,
               subject_id_list=[]):
    self.from_event = from_event
    self.to_event = to_event
    self.subject_id_list = subject_id_list
    self.condition = [de.category == "disease"]
    super(DiagnosisSankey, self).__init__()

  def query(self):
    # TODO:
    # string_agg(event_name, ', ' ORDER BY event_name) as from_event 변환
    tmp = session.\
        query(ce.subject_id,
              ce.ts,
              ce.event_id
              # case([(de.event_name == "myocardial_inf, ischemic_hd", "myocardial_inf")],
              #      else_=de.event_name).label("event_name")
              ).\
        distinct().\
        cte("tmp")

    if self.from_event or self.to_event:
      self.condition.append(or_(de.event_name == self.from_event,
                                de.event_name == self.to_event))
    query = session.\
        query(tmp.c.subject_id,
              tmp.c.ts.label("from_ts"),
              func.array_agg(tmp.c.event_id).label("from_event")
              # func.string_agg(de.event_name,
              #                 aggregate_order_by(literal_column(", "), de.event_name.desc())).label("from_event")
              ).\
        join(de, tmp.c.event_id == de.event_id).\
        filter(and_(*self.condition)).\
        group_by(tmp.c.subject_id, tmp.c.ts)
    self.result = pd.read_sql(query.statement, query.session.bind)

    return self

  def export(self):
    return super(DiagnosisSankey, self).to_json()


class LabSankey(Sankey):

  def __init__(self,
               from_event=None,
               to_event=None,
               subject_id_list=[]):
    self.from_event = from_event
    self.to_event = to_event
    self.subject_id_list = subject_id_list
    self.condition = [de.category == "lab"]
    super(LabSankey, self).__init__()

  def query(self):

    if self.from_event or self.to_event:
      self.condition.append(or_(de.event_name == self.from_event,
                                de.event_name == self.to_event))

    # TODO:
    # string_agg(event_name, ', ' ORDER BY event_name) as from_event 변환
    tmp = session.\
        query(ce.subject_id,
              ce.ts,
              ce.event_id
              ).\
        distinct().\
        cte("tmp")
    query = session.\
        query(tmp.c.subject_id,
              tmp.c.ts.label("from_ts"),  # TODO: date_trunc('day', e.ts) AS ts
              func.array_agg(tmp.c.event_id).label("from_event")
              # TODO: split_part(d.event_name, ':', 1) as event_name
              # func.string_agg(de.event_name,
              #                 aggregate_order_by(literal_column(", "), de.event_name.desc())).label("from_event")
              ).\
        join(de, tmp.c.event_id == de.event_id).\
        filter(and_(*self.condition)).\
        group_by(tmp.c.subject_id, tmp.c.ts)
    self.result = pd.read_sql(query.statement, query.session.bind)
    return self

  def export(self):
    return super(LabSankey, self).to_json()


class PrescriptionSankey(Sankey):

  def __init__(self,
               from_event=None,
               to_event=None,
               subject_id_list=[]):
    self.from_event = from_event
    self.to_event = to_event
    self.subject_id_list = subject_id_list
    self.condition = [de.category == "prescription"]
    super(PrescriptionSankey, self).__init__()

  def query(self):
    # TODO:
    # string_agg(event_name, ', ' ORDER BY event_name) as from_event 변환
    tmp = session.\
        query(ce.subject_id,
              ce.ts,
              ce.event_id
              ).\
        distinct().\
        cte("tmp")
    query = session.\
        query(tmp.c.subject_id,
              tmp.c.ts.label("from_ts"),
              func.array_agg(tmp.c.event_id).label("from_event")
              # TODO:
              # case
              #   when lower(d.event_name) SIMILAR TO '%%(atorvastatin|pitavastatin|lovastatin|
              #   simvastatin|pravastatin|fluvastatin|rosuvastatin)%%'
              #   then 'Statin'
              #   when lower(d.event_name) SIMILAR TO '%%(clopidogrel|ticlopidine|ticagrelor|prasugrel|cangrelor)%%'
              #   then 'P2Y12 inhibitor'
              #   when lower(d.event_name) SIMILAR TO '%%aspirin%%'
              #   then 'Aspirin'
              #   when lower(d.event_name) SIMILAR TO '%%(celecoxib|diclofenac|diflunisal|etodolac|ibuprofen|
              #   indomethacin|ketoprofen|ketorolac|nabumetone|naproxen|oxaprozin|piroxicam|salsalate|sulindac|tolmetin)%%'
              #   then 'NSAIDs'
              #   when lower(d.event_name) SIMILAR TO '%%(tacrolimus|cyclosporine|mycophenolate mofetil|
              #   mycophenolate sodium|azathioprine|sirolimus|prednisone)%%'
              #   then 'Immunosuppressant'
              #   else 'Others'
              # end as event_name
              # func.string_agg(de.event_name,
              #                 aggregate_order_by(literal_column(", "), de.event_name.desc())).label("from_event")
              ).\
        join(de, tmp.c.event_id == de.event_id).\
        filter(and_(*self.condition)).\
        group_by(tmp.c.subject_id, tmp.c.ts)
    self.result = pd.read_sql(query.statement, query.session.bind)
    return self

  def export(self):
    return super(PrescriptionSankey, self).to_json()


class DemographicByDiagnosisSankey(DiagnosisSankey):

  def __init__(self,
               from_event=None,
               to_event=None,
               subject_id_list=[]):
    super(DemographicByDiagnosisSankey, self).__init__(from_event, to_event, subject_id_list)

  def query(self):
    diagnosis = super(DemographicByDiagnosisSankey, self).query().preprocess().toDF()

    subject_id_list = set(diagnosis["subject_id"].tolist())

    query = session.query(cdemo).filter(cdemo.subject_id.in_(subject_id_list))

    self.result = pd.read_sql(query.statement, query.session.bind)
    return self

  def export(self):
    r = self.result.to_dict(orient="record")
    # TODO: use SankeyFormat
    return r


class AdmissionByDiagnosisSankey(DiagnosisSankey):

  def __init__(self,
               from_event=None,
               to_event=None,
               subject_id_list=[]):
    super(AdmissionByDiagnosisSankey, self).__init__(from_event, to_event, subject_id_list)

  def query(self):
    diagnosis = super(AdmissionByDiagnosisSankey, self).query().preprocess().toDF()

    subject_id_list = set(diagnosis["subject_id"].tolist())

    query = session.query(cadm).filter(cadm.subject_id.in_(subject_id_list))

    self.result = pd.read_sql(query.statement, query.session.bind)
    return self

  def export(self):
    r = self.result.to_dict(orient="record")
    # TODO: use SankeyFormat
    return r


class PrescriptionByDiagnosisSankey(DiagnosisSankey):

  def __init__(self,
               from_event,
               to_event,
               subject_id_list=[]):
    super(PrescriptionByDiagnosisSankey, self).__init__(from_event, to_event, subject_id_list)

  def query(self):
    diagnosis = super(PrescriptionByDiagnosisSankey, self).query().preprocess().toDF()

    subject_id_list = set(diagnosis["subject_id"].tolist())

    query = session.query(cpres).filter(cpres.subject_id.in_(subject_id_list))

    group_prescription = pd.read_sql(query.statement, query.session.bind)
    group_diag = diagnosis[["subject_id", "to_ts"]]
    self.result = pd.merge(group_prescription,
                           group_diag,
                           on="subject_id")
    self.result["diff_time"] = self.result["latest_date"] - self.result["to_ts"]
    return self

  def export(self):
    r = self.result.to_dict(orient="record")
    # TODO: use SankeyFormat
    return r


class LabByDiagnosisSankey(DiagnosisSankey):

  def __init__(self,
               from_event,
               to_event,
               subject_id_list=[]):
    super(LabByDiagnosisSankey, self).__init__(from_event, to_event, subject_id_list)

  def query(self):
    diagnosis = super(LabByDiagnosisSankey, self).query().preprocess().toDF()

    subject_id_list = set(diagnosis["subject_id"].tolist())

    query = session.query(clab).filter(clab.subject_id.in_(subject_id_list))

    group_lab = pd.read_sql(query.statement, query.session.bind)
    group_diag = diagnosis[["subject_id", "to_ts"]]
    self.result = pd.merge(group_lab,
                           group_diag,
                           on="subject_id")
    self.result["diff_time"] = self.result["charttime"] - self.result["to_ts"]
    return self

  def export(self):
    r = self.result.to_dict(orient="record")
    # TODO: use SankeyFormat
    return r


class ProcedureByDiagnosisSankey(DiagnosisSankey):

  def __init__(self,
               from_event,
               to_event,
               subject_id_list=[]):
    super(ProcedureByDiagnosisSankey, self).__init__(from_event, to_event, subject_id_list)

  def query(self):
    diagnosis = super(ProcedureByDiagnosisSankey, self).query().preprocess().toDF()

    subject_id_list = set(diagnosis["subject_id"].tolist())

    query = session.query(cproc).filter(cproc.subject_id.in_(subject_id_list))

    group_lab = pd.read_sql(query.statement, query.session.bind)
    group_diag = diagnosis[["subject_id", "to_ts"]]
    self.result = pd.merge(group_lab,
                           group_diag,
                           on="subject_id")
    self.result["diff_time"] = self.result["admittime"] - self.result["to_ts"]
    return self

  def export(self):
    r = self.result.to_dict(orient="record")
    # TODO: use SankeyFormat
    return r
