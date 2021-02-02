import spynnaker8 as p
import numpy as np
from python_models8.neuron.builds.zlif_curr_delta import ZLIFCurrDelta
from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon


# def test_ZLIFCurrDelta():
#     simulator = MockSimulator.setup()
#     model = ZLIFCurrDelta()
#     pop_1 = PyNNPopulationCommon(spinnaker_control=simulator, size=5,
#                                  label="Test", constraints=None, model=model,
#                                  structure=None, initial_values=None)
#     pop_1.set("v", 2)
#     values = pop_1.get("v")
#     assert [2, 2, 2, 2, 2] == values
#     values = pop_1.get_by_selector(slice(1, 3), "v")
#     assert [2, 2] == values
#     pop_1.set_by_selector(slice(1, 3), "v", 3)
#     values = pop_1.get("v")
#     assert [2, 3, 3, 2, 2] == values
#     values = pop_1.get(["cm", "v_thresh"])
#     assert [1.0, 1.0, 1.0, 1.0, 1.0] == values['cm']
#     assert [-50.0, -50.0, -50.0, -50.0, -50.0] == values["v_thresh"]
#     values = pop_1.get_by_selector([1, 3, 4], ["cm", "v_thresh"])
#     assert [1.0, 1.0, 1.0] == values['cm']
#     assert [-50.0, -50.0, -50.0] == values["v_thresh"]

def test_ZLIFCurrDelta_live():
    '''Test to see if C code is giving the right answers from machine'''
    p.setup(time_scale_factor=1, timestep=1)

    input = p.Population(1, p.SpikeSourceArray(list(range(0, 1000, 5))))
    pop = p.Population(1, ZLIFCurrDelta(v=1.0), {})
    
    proj = p.Projection(input, pop, p.AllToAllConnector(), p.StaticSynapse(weight=1), receptor_type='inhibitory')

    pop.record('v')

    p.run(1000)

    v_trace = pop.get_data('v')
    p.end()

    import matplotlib.pyplot as plt

    plt.plot(np.squeeze(np.array(v_trace.segments[0].analogsignals)))
    plt.show()


def test_ZLIFCurrDelta_voltage_clipping():

    p.setup(time_scale_factor=1, timestep=1)

    input = p.Population(1, p.SpikeSourceArray(list(range(0, 256, 1))))
    pop = p.Population(1, ZLIFCurrDelta(v=0))

    proj = p.Projection(input, pop, p.AllToAllConnector(), p.StaticSynapse(weight=1), receptor_type='inhibitory')

    pop.record('v')

    p.run(2560)

    v_trace = pop.get_data('v')


    p.end()

    v_trace = np.array(v_trace.segments[0].analogsignals)
    assert v_trace[-1] == -128


def test_ZLIFCurrDelta_membrane_addition():

    p.setup(time_scale_factor=1, timestep=1)

    input = p.Population(2, p.SpikeSourceArray([[10], [20]]))
    pop = p.Population(1, ZLIFCurrDelta(v=0))

    proj = p.Projection(input, pop, p.FromListConnector([(0,0,10,0), (1,0,20,0)]), receptor_type='excitatory')

    pop.record('v')

    p.run(100)

    v_trace = pop.get_data('v')


    p.end()

    v_trace = np.array(v_trace.segments[0].analogsignals)
    assert v_trace[-1] == 30




def test_ZLIFCurrDelta_threshold():

    p.setup(time_scale_factor=1, timestep=1)

    input = p.Population(1, p.SpikeSourceArray(list(range(0, 64, 1))))
    pop = p.Population(1, ZLIFCurrDelta(v=0, v_thresh=64))

    proj = p.Projection(input, pop, p.AllToAllConnector(), p.StaticSynapse(weight=1), receptor_type='excitatory')

    pop.record('v')

    p.run(66)

    v_trace = pop.get_data('v')


    p.end()

    v_trace = np.squeeze(np.array(v_trace.segments[0].analogsignals))

    import matplotlib.pyplot as plt

    plt.plot(v_trace)
    plt.show()


    assert v_trace[-1] == 0





if __name__ == '__main__':
    test_ZLIFCurrDelta_voltage_clipping()
    test_ZLIFCurrDelta_membrane_addition()
    test_ZLIFCurrDelta_threshold()