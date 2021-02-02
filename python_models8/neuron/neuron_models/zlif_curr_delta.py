from spinn_front_end_common.utilities.constants import \
    MICRO_TO_MILLISECOND_CONVERSION
from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spynnaker.pyNN.models.neuron.neuron_models import AbstractNeuronModel

I_OFFSET = "i_offset"
V = "v"
V_reset = "v_reset"


UNITS = {
    I_OFFSET: "nA",
    V: "mV",
    V_reset: "mV"
}


class ZLIFCurr(AbstractNeuronModel):
    def __init__(self, v, v_reset, i_offset):
        super(ZLIFCurr, self).__init__(
            data_types=[
                DataType.S1615, # v
                DataType.S1615, # v_reset
                DataType.S1615], #i_offset
            global_data_types=[
                DataType.UINT32   # machine_time_step
                ])

        self._i_offset = i_offset
        self._v = v
        self._v_reset = v_reset


    @property
    def i_offset(self):
        return self._i_offset

    @i_offset.setter
    def i_offset(self, i_offset):
        self._i_offset = i_offset


    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v_ = v

    @property
    def v_reset(self):
        return self._v_reset

    @v_reset.setter
    def v_reset(self, v_reset):
        self._v_reset = v_reset

    @overrides(AbstractNeuronModel.get_n_cpu_cycles)
    def get_n_cpu_cycles(self, n_neurons):
        # TODO: Calculate (or guess) the CPU cycles
        return 10 * n_neurons

    @overrides(AbstractNeuronModel.add_parameters)
    def add_parameters(self, parameters):
        parameters[I_OFFSET] = self._i_offset
        parameters[V_reset] = self._v_reset
        parameters[V] = self._v

    @overrides(AbstractNeuronModel.add_state_variables)
    def add_state_variables(self, state_variables):
        state_variables[V] = self._v

    @overrides(AbstractNeuronModel.get_values)
    def get_values(self, parameters, state_variables, vertex_slice, ts):
        # state variables, or other
        return [state_variables[V],
                parameters[V_reset],
                parameters[I_OFFSET]]

    @overrides(AbstractNeuronModel.get_global_values)
    def get_global_values(self, ts):
        return [float(ts) / MICRO_TO_MILLISECOND_CONVERSION]

    @overrides(AbstractNeuronModel.update_values)
    def update_values(self, values, parameters, state_variables):
        # the parameters and state variables
        (v, _i_offset) = values

        # NOTE: If you know that the value doesn't change, you don't have to
        # assign it (hint: often only state variables are likely to change)!
        state_variables[V] = v


    @overrides(AbstractNeuronModel.has_variable)
    def has_variable(self, variable):
        # This works from the UNITS dict, so no changes are required
        return variable in UNITS

    @overrides(AbstractNeuronModel.get_units)
    def get_units(self, variable):
        # This works from the UNITS dict, so no changes are required
        return UNITS[variable]
