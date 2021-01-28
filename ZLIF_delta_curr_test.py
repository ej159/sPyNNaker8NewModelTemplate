import spynnaker8 as p
from python_models8.neuron.builds.zlif_curr_delta import ZLIFCurrDelta

p.setup()

pop = p.Population(1, ZLIFCurrDelta, {})