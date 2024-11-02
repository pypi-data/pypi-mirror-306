from typing import Callable, Dict, Optional, Union
from pipium_connect.connect_model import ConnectionInput, ConnectionModel
from pipium_connect.run_observer_model import RunObserver
from pipium_connect.run_value_model import RunValue


# A single Connection to Pipium, containing run functions and any `ConnectionModel` configuration.
class Connection(ConnectionModel):
    # Run function that returns one or more values.
    # @param input Input data for the run, containing input binary data, configuration and previous values for this run.
    # @returns One or more `RunValue`, such as binary data or plain text.
    run_sync: Optional[
        Callable[
            [ConnectionInput],
            Union[RunValue, list[RunValue]],
        ]
    ] = None

    # Run function that emits values, errors and completion notifications.
    # @param input Input data for the run, containing input binary data, configuration and previous values for this run.
    # @param observer Observer for the run, containing methods to emit values, errors and completion notifications.
    run_async: Optional[Callable[[ConnectionInput, RunObserver], None]] = None


# A collection of `Connection` objects, indexed by their unique ID.
Connections = Dict[str, Connection]
