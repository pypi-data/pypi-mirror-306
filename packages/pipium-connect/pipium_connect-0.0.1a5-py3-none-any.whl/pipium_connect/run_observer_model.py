from typing import Callable
from pipium_connect.run_value_model import RunValue


# An observer contains callbacks that handle the three possible outcomes of a run:
# - next: the run has produced a value
# - error: the run has produced an error and stopped
# - complete: the run has completed and will not produce any more values
class RunObserver:
    next: Callable[[RunValue], None]
    error: Callable[[str], None]
    complete: Callable[[], None]
