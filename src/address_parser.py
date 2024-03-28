MAX_SPLITS = 1

def parse_file(filepath: str) -> list[str]:
  """
  Parses a text file into a list of strings where newlines occur. In 
  addition leading/trailing whitespace are removed from entries, as well as empty strings. 

  Args:
      filepath: The path to the text file.

  Returns:
      A list of strings, where each element is a stripped line from the file.
  """
  with open(filepath, 'r') as file:
    entries = file.readlines()

  return _clean(_trim(entries))

def split_address(input: str, split_token: str) -> tuple[str, str]:
  """
  Splits an input string in to two strings at the first occurrence of split_token.

  Args:
    input: The string to be split.
    split_token: the substring where the split is to take place.

  Returns:
    A two-tuple consisting of the split string or the entire string in the left indice
    if the substring "split-token" could not be found.
  """
  two_parts = input.split(split_token, MAX_SPLITS)
  if len(two_parts) == 2: return two_parts[0], two_parts[1]
  else: return two_parts[0], ""

def _trim(lines: list[str]) -> list[str]:
  return list(map(lambda entry: str.strip(entry), lines))

def _clean(lines: list[str]) -> list[str]:
  return list(filter(lambda entry: bool(entry), lines))