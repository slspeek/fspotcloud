from webfront.models import State

def set_value(var_name, value):
  if has_var(var_name):
    var = find_var(var_name)
  else:
    var = State(key_name=var_name)
  var.value = value
  var.put()
  
def get_value(var_name):
  if has_var(var_name):
    var = find_var(var_name)
  else: 
    return None
  return var.value

def find_var(var_name):
  return State.get_by_key_name(var_name)

def has_var(var_name):
  return find_var(var_name) != None
