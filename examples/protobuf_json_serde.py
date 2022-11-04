from google.protobuf import json_format

from registry.order_placed_event_pb2 import OrderPlaced

# Build Message structure
message = OrderPlaced(id=123, price=13.99, quantity=1, product_id=10001)
print(message)

# Default serialization in protobuf is binary - message.SerializeToString()
# b'\x08{\x10\x91N\x1d\n\xd7_A \x01'

# We can use protobuf with JSON though and keep messages to be human-readable.

# From Message to JSON
print("Serializing message to JSON")
serialized_as_json = json_format.MessageToJson(
    message, including_default_value_fields=True
)
#                                              this is required to get all fields  ☝
print(serialized_as_json)

# From JSON to message
print("Deserializing message from JSON")
new_message = OrderPlaced()
deserialized_from_json = json_format.Parse(serialized_as_json, new_message)
print(deserialized_from_json)
