
def window(iterable, size=2):
  try:
    i = iter(iterable)
    win = []
    for e in range(0, size):
      win.append(next(i))
    yield win
    for e in i:
      win = win[1:] + [e]
      yield win
  except StopIteration:
    return


def pathway(result=None):
  """window함수를 적용하여 질병을 순차적으로 2개씩 묶은 리스트 tuples 생성
  """

  if result is None:
    return []
  pathway_list = []

  for i in result:
    try:
      for source, target in window(result[i]):
        pathway_list.append(
            dict(subject_id=i,
                 source="".join(source),
                 target="".join(target)))
    except Exception:
        pass
  return pathway_list


def print_compiled_stmt(statement):
  """
  print compiled statement
  """
  print(str(statement.compile(compile_kwargs={"literal_binds": True})))
