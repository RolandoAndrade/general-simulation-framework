import unittest
from time import sleep
from random import random, seed

from control.controls.discrete_event_control import DiscreteEventControl
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from reports.report_generators.default_report import DefaultReport
from simulation.simulation_engines.discrete_event_simulation_engine import (
    DiscreteEventSimulationEngine,
)
from test.model.drill.drill import Drill
from test.model.drill.press import Press


class TestDrill(unittest.TestCase):
    def test_table(self):
        ds = DiscreteEventDynamicSystem()
        press = Press(ds, "Press 1")
        drill = Drill(ds, "Drill 1")
        press.add(drill)

        inputs = [
            {press.getID(): {"ext": 1}},
            {press.getID(): {"ext": 2}},
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
            print("output -> " + str(ds.getOutput()))
            print("--")
            if i < 1:
                ds.stateTransition(inputs[i], 0)
            else:
                ds.stateTransition(inputs[i], ds.getTimeOfNextEvent())
            print(str(press))
            print(str(drill))
            print("--")
            print(ds._scheduler)
            if ds.getTimeOfNextEvent() == 0:
                break
            i = i + ds.getTimeOfNextEvent()

    def test_network(self):
        ds = DiscreteEventDynamicSystem()
        press1 = Press(ds, "Press 1")
        press2 = Press(ds, "Press 2")
        drill = Drill(ds, "Drill")
        press1.add(drill)
        press2.add(drill)

        inputs = [
            {press1.getID(): {"ext": 1}, press2.getID(): {"ext": 2}},
            {press1.getID(): {"ext": 2}, press2.getID(): {"ext": 3}},
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
            print("output -> " + str(ds.getOutput()))
            print("--")
            if i < 1:
                ds.stateTransition(inputs[i], 0)
            else:
                ds.stateTransition(inputs[i], ds.getTimeOfNextEvent())
            print(str(press1))
            print(str(press2))
            print(str(drill))
            print("--")
            print(ds._scheduler)
            if ds.getTimeOfNextEvent() == 0:
                break
            i = i + ds.getTimeOfNextEvent()

    def test_simple_simulation(self):
        ds = DiscreteEventDynamicSystem()
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
                k = {press.getID(): {"ext": 1}}
                print("Inserting 1 element in time " + str(time))
            engine.computeNextState(k, time)
        print(report.generateReport())

    def test_add_remove(self):
        ds = DiscreteEventDynamicSystem()
        press1 = Press(ds, "Press 1")
        press2 = Press(ds, "Press 2")
        drill = Drill(ds, "Drill")
        press1.add(drill)
        press2.add(drill)

        self.assertTrue(len(press1.getOutputModels()) == 1, "It should have an output")
        self.assertTrue(len(press2.getOutputModels()) == 1, "It should have an output")

        press2.remove(drill)

        self.assertTrue(len(press1.getOutputModels()) == 1, "It should have an output")
        self.assertTrue(len(press2.getOutputModels()) == 0, "It should have no outputs")

        ds.remove(drill)

        self.assertTrue(len(press1.getOutputModels()) == 0, "It should have no outputs")
        self.assertTrue(len(press2.getOutputModels()) == 0, "It should have no outputs")

    def test_control(self):
        ds = DiscreteEventDynamicSystem()
        report = DefaultReport()
        engine = DiscreteEventSimulationEngine(ds, report)
        control = DiscreteEventControl(engine)
        press = Press(ds, "Press 1")
        drill = Drill(ds, "Drill 1")
        press.add(drill)
        k = {press.getID(): {"ext": 1}}
        control.start(k)
        sleep(0.1)
        print(report.generateReport())
        control.stop()


if __name__ == "__main__":
    unittest.main()
