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

#ifndef _NEURON_MODEL_LIF_CURR_IMPL_H_
#define _NEURON_MODEL_LIF_CURR_IMPL_H_

#include <neuron/models/neuron_model.h>

typedef struct neuron_t {
    // TODO: Parameters - make sure these match with the Python code,
    // including the order of the variables when returned by
    // get_neural_parameters.

    // Variable-state parameters e.g. membrane voltage
    int8_t V_membrane;

    //! post-spike reset membrane voltage [mV]
    int8_t V_reset;

    // offset current [nA]
    int8_t I_offset;

} neuron_t;

typedef struct global_neuron_params_t {
    // TODO: Add any parameters that apply to the whole model here (i.e. not
    // just to a single neuron)

    // Note: often these are not user supplied, but computed parameters

    uint32_t machine_time_step;
} global_neuron_params_t;

#endif // _NEURON_MODEL_MY_IMPL_H_
