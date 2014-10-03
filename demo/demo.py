# statements will be unjoined
hash_table = {
  'key-1': 'value-1',
  'key-2': 'value-2',
  'key-3': 'value-3'
}

boolean = (
  1 > 2 and
  some_variable > another_variable or
  method_call(a1 + a2)
)

# statements will be joined
hash_table = {'key-1': 'value-1', 'key-2': 'value-2', 'key-3': 'value-3'}
boolean = (1 > 2 and some_variable > another_variable or method_call(a1 + a2))

# profit =)