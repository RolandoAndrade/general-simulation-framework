import unittest
from time import sleep
from random import random, seed

from control.controls.discrete_event_control import DiscreteEventControl
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from reports.report_generators.default_report import DefaultReport
from simulation.simulation_engines.discrete_event_simulation_engine import (
    DiscreteEventSimulationEngine,
)
from test.model.drill.drill import Drill
from test.model.drill.factory_system import FactorySystem
from test.model.drill.press import Press


class TestDrill(unittest.TestCase):
    def test_table(self):
        ds = FactorySystem()
        press = Press(ds, "Press 1")
        drill = Drill(ds, "Drill 1")
        press.add(drill)

        inputs = [
            {press.get_id(): {"ext": 1}},
            {press.get_id(): {"ext": 2}},
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        i = 0
        while True:
            print("------------------")
            print("time -> " + str(i))
            if inputs[i] is not None:
                print("Inserting " + str(inputs[i]["Press 1"]["ext"]) + " part(s)")
            print("output -> " + str(ds.get_output()))
            print("--")
            if i < 1:
                ds.state_transition(inputs[i], 0)
            else:
                ds.state_transition(inputs[i], ds.get_time_of_next_events())
            print(str(press))
            print(str(drill))
            print("--")
            print(ds._scheduler)
            if ds.get_time_of_next_events() == 0:
                break
            i = i + ds.get_time_of_next_events()

    def test_network(self):
        ds = FactorySystem()
        press1 = Press(ds, "Press 1")
        press2 = Press(ds, "Press 2")
        drill = Drill(ds, "Drill")
        press1.add(drill)
        press2.add(drill)

        inputs = [
            {press1.get_id(): {"ext": 1}, press2.get_id(): {"ext": 2}},
            {press1.get_id(): {"ext": 2}, press2.get_id(): {"ext": 3}},
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        i = 0
        while True:
            print("------------------")
            print("time -> " + str(i))
            if inputs[i] is not None:
                print("Inserting " + str(inputs[i]["Press 1"]["ext"]) + " part(s)")
            print("output -> " + str(ds.get_output()))
            print("--")
            if i < 1:
                ds.state_transition(inputs[i], 0)
            else:
                ds.state_transition(inputs[i], ds.get_time_of_next_events())
            print(str(press1))
            print(str(press2))
            print(str(drill))
            print("--")
            print(ds._scheduler)
            if ds.get_time_of_next_events() == 0:
                break
            i = i + ds.get_time_of_next_events()

    def test_simple_simulation(self):
        ds = FactorySystem()
        report = DefaultReport()
        engine = DiscreteEventSimulationEngine(ds, report)
        press = Press(ds, "Press 1")
        drill = Drill(ds, "Drill 1")
        press.add(drill)
        seed(42)
        for time in range(10):
            x = random()
            k = None
            if x < 0.3:
                k = {press.get_id(): {"ext": 1}}
                print("Inserting 1 element in time " + str(time))
            engine.compute_next_state(k, time)
        print(report.generate_report())

    def test_add_remove(self):
        ds = FactorySystem()
        press1 = Press(ds, "Press 1")
        press2 = Press(ds, "Press 2")
        drill = Drill(ds, "Drill")
        press1.add(drill)
        press2.add(drill)

        self.assertTrue(len(press1.get_output_models()) == 1, "It should have an output")
        self.assertTrue(len(press2.get_output_models()) == 1, "It should have an output")

        press2.remove(drill)

        self.assertTrue(len(press1.get_output_models()) == 1, "It should have an output")
        self.assertTrue(len(press2.get_output_models()) == 0, "It should have no outputs")

        ds.remove(drill)

        self.assertTrue(len(press1.get_output_models()) == 0, "It should have no outputs")
        self.assertTrue(len(press2.get_output_models()) == 0, "It should have no outputs")

    def test_control(self):
        ds = FactorySystem()
        report = DefaultReport()
        engine = DiscreteEventSimulationEngine(ds, report)
        control = DiscreteEventControl(engine)
        press = Press(ds, "Press 1")
        drill = Drill(ds, "Drill 1")
        press.add(drill)
        k = {press.get_id(): {"ext": 1}}
        control.start(k)
        sleep(0.1)
        print(report.generate_report())
        control.stop()

    def test_experiment(self):
        ds = FactorySystem()
        press = Press(ds, "Press 1")
        drill = Drill(ds, "Drill 1")
        press.add(drill)
        experiment = DiscreteEventExperiment(ds)
        k = {press.get_id(): {"ext": 2}}
        experiment.simulation_control.start(k)
        sleep(0.1)
        print(experiment.simulation_report.generate_report())
        experiment.simulation_control.stop()


if __name__ == "__main__":
    unittest.main()
