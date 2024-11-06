import os
import traceback
from positron_common.deployment.stored_function import StoredFunction
from positron_common.user_config import REMOTE_FUNCTION_SECRET_KEY_NAME

def _get_from_disk(path: str):
  with open(path, "rb") as f:
    return f.read()

def _write_to_disk(path: str, data: bytes):
  with open(path, "wb") as f:
    f.write(data)

def app():
  """Reads the function parts from disk and executes."""

  print('Reading function parts from disk...')
  s_func = _get_from_disk(f"function.pkl")
  s_args = _get_from_disk(f"args.pkl")
  s_kwargs = _get_from_disk(f"kwargs.pkl")

  stored_function = StoredFunction()
  stored_function.s_func = s_func
  stored_function.s_args = s_args
  stored_function.s_kwargs = s_kwargs

  print('Deserializing function and args...')
  stored_function.deserialize_function()

  print('Executing function...')
  stored_function.run()

  print('Serializing results...')
  hmac_key = os.environ[REMOTE_FUNCTION_SECRET_KEY_NAME]
  stored_function.serialize_results()
  # Tradeoff, we can put this here to be quicker overall, but it does add procesing
  # on the users dime. Plus, we have to pass down the hmac_key to the process.
  stored_function.create_results_metadata(hmac_key=hmac_key)
  if stored_function.result is not None:
    print(f"Results: {stored_function.result}")
    _write_to_disk(f"result.pkl", stored_function.s_result)
  if stored_function.exception is not None:
    traceback.print_exception(type(stored_function.exception), stored_function.exception, stored_function.exception.__traceback__)
    print(f"Exception: {stored_function.exception}")
    _write_to_disk(f"exception.pkl", stored_function.s_exception)

  results_metadata = stored_function.s_meta.to_json()
  _write_to_disk(f"results_metadata.json", results_metadata)

  print('Done!')

if __name__ == "__main__":
  app()
