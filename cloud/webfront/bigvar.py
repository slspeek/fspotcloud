from webfront.models import State

def set_value(var_name, value):
  if has_var(var_name):
    var = find_var(var_name)
  else:
    var = State(var=var_name)
  var.value = value
  var.put()
  
def get_value(var_name):
  if has_var(var_name):
    var = find_var(var_name)
  else: 
    return None
  return var.value

def find_var(var_name):
  return State.gql('WHERE var = :1', var_name).fetch(1)[0]

def has_var(var_name):
  return State.gql('WHERE var = :1', var_name).count(2) > 0
