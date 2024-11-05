"""Baseline removal steps for use with the Processing Pipeline.

Classes
-------
FIRBaselineCorrection
    Baseline removal based on a FIR lowpass filter.
"""

import logging
from collections.abc import Sequence

from scipy.signal import filtfilt, firwin, kaiserord

from pyProcessingPipeline.exceptions import ProcessingError
from pyProcessingPipeline.steps._base import ProcessingStep
from pyProcessingPipeline.steps._step_identifiers import StepIdentifier
from pyProcessingPipeline.types import FloatArray, ProcessingStepInput

logger = logging.getLogger(__name__)


class FaultyFilterParameterError(ProcessingError):
    """Thrown if the given filter parameters are nonsensical."""

    def __init__(self, passband: float, stopband: float) -> None:
        super().__init__(
            "Stopband frequency must be smaller than the passband frequency! "
            + f"Passband {passband} is not smaller than stopband {stopband}"
        )


class FIRBaselineCorrection(ProcessingStep):
    """Baseline correction using a finite impulse response lowpass filter.

    Example
    -------

    To remove a low frequency baseline component from a signal,
    first create a processing run:

    >>> from pyProcessingPipeline import ProcessingRun
    >>> processing_run = ProcessingRun(
    ...     name="ExampleRun",
    ...     description="Run that lowpass filters a signal",
    ... )

    And add the baseline correction step:

    >>> processing_run.add_step(
    ...     FIRBaselineCorrection(
    ...         sampling_frequency=1000/20,
    ...         passband_frequency=2.5,
    ...         stopband_frequency=1.2,
    ...         stopband_attenuation=60,
    ...     )
    ... )

    To test this step, we will use a simple signal consisting of
    two superpositioned sine waves, where we want to remove
    the lower frequency baseline component

    >>> import numpy as np
    >>> x = np.linspace(0, 20 * 2*np.pi, 1000)
    >>> baseline = np.sin(x)
    >>> signal = baseline + np.sin(3*x)

    Currently, the signals difference from a signal without
    a baseline is

    >>> round(np.mean(abs(signal - np.sin(3*x))), 2)
    0.64

    To remove this signals baseline, start the processing run:

    >>> processing_run.run([signal])

    The filtered signal is now available in the results:

    >>> result = processing_run.results[0]

    and its average difference to the expected signal is now

    >>> round(np.mean(abs(result - np.sin(3*x))), 2)
    0.0
    """

    _sampling_frequency: float
    _passband_frequency: float
    _stopband_attenuation: float
    _stopband_frequency: float
    _kaiser_window: FloatArray

    def __init__(
        self,
        sampling_frequency: float,
        passband_frequency: float,
        stopband_frequency: float,
        stopband_attenuation: float,
    ):
        """Create a baseline correction step.

        Parameters
        ----------
        sampling_frequency : float
            Sampling frequency of the signal in Hz.
        passband_frequency : float
            Passband frequency of the lowpass filter,
            used for calculating the baseline, in Hz.
        stopband_frequency : float
            Stopband of the filter in Hz.
        stopband_attenuation : float
            Signal attenuation in the stop band, in dB.
        """
        super().__init__(locals())

        if passband_frequency < stopband_frequency:
            raise FaultyFilterParameterError(
                passband=passband_frequency, stopband=stopband_frequency
            )

        self._sampling_frequency = sampling_frequency
        self._passband_frequency = passband_frequency
        self._stopband_frequency = stopband_frequency
        self._stopband_attenuation = stopband_attenuation

        kaiser_taps, kaiser_beta = kaiserord(
            ripple=self._stopband_attenuation,
            width=2
            * (self._passband_frequency - self._stopband_frequency)
            / self._sampling_frequency,
        )

        if kaiser_taps % 2 == 0:
            kaiser_taps = kaiser_taps + 1

        self._kaiser_window = firwin(
            numtaps=kaiser_taps,
            cutoff=(self._passband_frequency + self._stopband_frequency) / 2,
            fs=self._sampling_frequency,
            pass_zero="lowpass",
            window=("kaiser", kaiser_beta),
        )

    @staticmethod
    def identifier() -> StepIdentifier:
        return StepIdentifier.PREPROCESSING_BASELINE_CORRECTION_FIR

    def run(
        self,
        step_input: ProcessingStepInput,
        labels: Sequence[str | None] | None = None,
    ) -> None:
        self._init_results()

        output_index = 0

        for input_index, item in enumerate(step_input.data):
            try:
                baseline = filtfilt(b=self._kaiser_window, a=1.0, x=item)
                result = item - baseline
            except Exception as error:
                print("Could not filter signal", input_index, error)
                self._input_mapping[input_index] = None
            else:
                self._data.append(result)
                self._input_mapping[input_index] = output_index
                output_index += 1
