"""Steps for splitting timeseries.

Classes
-------
Split
    Used for splitting a timeseries into multiple
    sub-series with the same length.
"""

import itertools
import logging
from collections import defaultdict
from collections.abc import Sequence

from pyProcessingPipeline.exceptions import ProcessingError
from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput
from pyProcessingPipeline.util import batch_generator

logger = logging.getLogger(__name__)


class UnableToSplitError(ProcessingError):
    """Raised if unable to split the given input."""

    def __init__(self, *args: object) -> None:
        message = """Unable to split input.
        Make sure all inputs have the same length, e.g.
        using the 'Cut' step."""
        super().__init__(message, *args)


class Split(ProcessingStep):
    """Split a timeseries into equal sub-series.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals_to_split = [
    ...     [1, 2, 3, 4, 5, 6],
    ...     [6, 5, 4, 3, 2, 1],
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal splitter",
    ... )
    ... # Split each signal into 2 subsignals
    >>> processing_run.add_step(Split(2))
    >>> processing_run.run(signals_to_split)
    >>> processing_run.results
    [array([1, 2, 3]), array([4, 5, 6]), array([6, 5, 4]), array([3, 2, 1])]

    If the input signals can not be evenly divided into
    n splits, the unsplittable arrays are dropped.

    >>> from pyProcessingPipeline import ProcessingRun
    >>> signals_to_split = [
    ...     [1, 2, 3, 4, 5],
    ...     [5, 4, 3, 2, 1],
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal splitter",
    ... )
    ... # Split each signal into 2 subsignals
    >>> processing_run.add_step(Split(2))
    >>> processing_run.run(signals_to_split)
    >>> processing_run.results
    [array([1, 2]), array([3, 4]), array([5, 4]), array([3, 2])]

    Here, the output is missing '5' from the first array,
    and '1' from the second.

    The input mapping shows which input got mapped to which outputs:

    >>> processing_run.steps[0].input_mapping
    {0: [0, 1], 1: [2, 3]}

    # Interlacing

    The optional `interlacing` parameter allows to create interlaced
    splits of multiple timeseries. This can be undone using the
    Unite step with the same interlacing parameter.

    >>> signals_to_split = [
    ...     [1, 2, 3, 4],
    ...     [5, 6, 7, 8],
    ...     [9, 10, 11, 12]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal splitter",
    ... )
    ... # Split each signal into 2 subsignals
    >>> processing_run.add_step(Split(2, 3))
    >>> processing_run.run(signals_to_split)
    >>> processing_run.results
    [array([1, 2]), array([5, 6]), array([ 9, 10]), array([3, 4]), array([7, 8]), array([11, 12])]

    The io mapping should represent the input getting split and interlaced
    into multiple output series:
    >>> processing_run.steps[0].input_mapping
    {0: [0, 3], 1: [1, 4], 2: [2, 5]}

    When choosing an interlacing amount that does not cleanly
    divide the amount of given input signals, extra signals
    will be dropped:

    >>> signals_to_split = [
    ...     [1, 2, 3, 4],
    ...     [5, 6, 7, 8],
    ...     [9, 10, 11, 12]
    ... ]
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that uses the signal splitter",
    ... )
    ... # Split each signal into 2 subsignals
    >>> processing_run.add_step(Split(2, 2)) # Interlacing of 2 will drop the last series
    >>> processing_run.run(signals_to_split)
    >>> processing_run.results
    [array([1, 2]), array([5, 6]), array([3, 4]), array([7, 8])]

    >>> processing_run.steps[0].input_mapping
    {0: [0, 2], 1: [1, 3]}

    """

    _num_sub_series: int
    _interlacing: int

    def __init__(
        self,
        number_of_sub_series: int,
        interlacing: int = 1,
    ):
        """Split a timeseries into n equal subseries.

        Parameters
        ----------
        number_of_sub_series : int
            Amount of sub-series to create from the input.
        interlacing : int, Optional, default 1
            Sets the interlacing amount of the split step.
            An interlacing of 1 will output consecutive splits,
            while any other number will interlace the splits of
            `interlacing` timeseries with each other.
        """
        super().__init__(locals())

        self._num_sub_series = number_of_sub_series
        self._interlacing = interlacing

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.MISC_SPLIT

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        # Warn the user if the input is not cleanly divisible by n
        if len(step_input.data) % self._interlacing != 0:
            logger.warning(
                "Input %s is not cleanly divisible by %s. Dropping extra entries.",
                str(len(step_input.data)),
                str(self._interlacing),
            )
            input_length = len(step_input.data) // self._interlacing * self._interlacing
            # Set input/output mapping for dropped values to None
            for input_index in range(input_length, len(step_input.data)):
                self._input_mapping[input_index] = None
        else:
            input_length = len(step_input.data)

        self._init_results()

        try:
            # Create interlaced ands split items using map and zip magic
            interlaced_batches = batch_generator(
                list(map(self._split, step_input.data[:input_length])),
                self._interlacing,
            )
            # Extend output data by those values.
            for batch in interlaced_batches:
                self._data.extend(
                    itertools.chain.from_iterable(zip(*batch, strict=True))
                )

            # Also set input/output mapping
            temp_mapping = defaultdict(list)
            for output_index in range(self._num_sub_series * input_length):
                input_index = (
                    output_index % self._interlacing
                    + (output_index // (self._num_sub_series * self._interlacing))
                    * self._interlacing
                )
                temp_mapping[input_index].append(output_index)
            self._input_mapping = dict(temp_mapping)

        except Exception as err:
            # Delete all temporary results
            self._init_results()
            # And raise an Error
            raise UnableToSplitError from err

    def _split(self, data: FloatArray) -> list[FloatArray]:
        """Split the given array into equal sub-arrays.

        Return a list of sub arrays.

        Parameters
        ----------
        data : FloatArray
            The array to split.

        Returns
        -------
        list[FloatArray]
            The split arrays.
        """
        length_of_split = len(data) // self._num_sub_series
        logger.info("Using split length of %s", length_of_split)
        results: list[FloatArray] = []
        for i in range(self._num_sub_series):
            left_index = i * length_of_split
            right_index = left_index + length_of_split
            results.append(data[left_index:right_index])
        return results
