# A PyNN Model for standard neurons built from components
from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModelStandard

# Components from main tools
from spynnaker.pyNN.models.neuron.input_types import InputTypeDelta
from spynnaker.pyNN.models.neuron.synapse_types import SynapseTypeDelta
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic

# Additional components
from spynnaker.pyNN.models.defaults import default_initial_values
from python_models8.neuron.neuron_models.zlif_curr_delta import ZLIFCurr


class ZLIFCurrDelta(AbstractPyNNNeuronModelStandard):

    # Identify which of the values are state variables
    @default_initial_values({"v", "isyn_exc", "isyn_inh"})
    def __init__(
            self, v_reset=0,
            v_thresh=64, i_offset=0.0, v=0,
            isyn_exc=0.0, isyn_inh=0.0):

        neuron_model = ZLIFCurr(
            v, i_offset, v_reset)
        synapse_type = SynapseTypeDelta(isyn_exc, isyn_inh)
        input_type = InputTypeDelta()
        threshold_type = ThresholdTypeStatic(v_thresh)


        # Create the model using the superclass
        super(ZLIFCurrDelta, self).__init__(

            # the model a name (shown in reports)
            model_name="ZLIFCurrDelta",

            # the matching binary name
            binary="zlif_curr_delta.aplx",

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type)
