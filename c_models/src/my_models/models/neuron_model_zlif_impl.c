/*
 * Copyright (c) 2017-2019 The University of Manchester
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "neuron_model_zlif_impl.h"

#include <debug.h>
#include <limits.h>

// The global parameters of this neuron model
static const global_neuron_params_t *global_params;

void neuron_model_set_global_neuron_params(
        const global_neuron_params_t *params) {

    global_params = params;
}

static inline void safe_input_add(
        neuron_t *neuron, int V_prev, input_t input_this_timestep) {
        // Does an overflow checking addition of input with clipping if input would underflow
        if ((V_prev < 0) && (input_this_timestep < INT_MIN - V_prev)) {
            neuron->V = INT_MIN;
        } else {
            neuron->V += input_this_timestep;
        }
}


state_t neuron_model_state_update(
        uint16_t num_excitatory_inputs, const input_t* exc_input,
        uint16_t num_inhibitory_inputs, const input_t* inh_input,
        input_t external_bias, neuron_t *restrict neuron) {

    // This takes the input and generates an input value, assumed to be a
    // current.  Note that the conversion to current from conductance is done
    // outside of this function, so does not need to be repeated here.

    // Sum contributions from multiple inputs (if used)
    REAL total_exc = 0;
    REAL total_inh = 0;
    for (uint32_t i = 0; i < num_excitatory_inputs; i++) {
        total_exc += exc_input[i];
    }
    for (uint32_t i = 0; i < num_inhibitory_inputs; i++) {
        total_inh += inh_input[i];
    }

    input_t input_this_timestep =
            total_exc - total_inh + external_bias + neuron->I_offset;

    safe_input_add(
        neuron, neuron->V, input_this_timestep);


    log_debug("TESTING TESTING V = %11.4k mv", neuron->V);

    // Return the state variable to be compared with the threshold value
    // to determine if the neuron has spikes (commonly the membrane voltage)

    return neuron->V;
}


state_t neuron_model_get_membrane_voltage(const neuron_t *neuron) {
    return neuron->V;
}

void neuron_model_has_spiked(neuron_t *restrict neuron) {
    neuron->V = neuron->V_reset;
}

void neuron_model_print_state_variables(const neuron_t *neuron) {
    log_debug("V = %11.4k mv", neuron->V);
}