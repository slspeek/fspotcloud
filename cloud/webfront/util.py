def ceil_divide(x, y):
  result = x // y
  if not x % y == 0:
    result += 1
  return result
