import unittest

from core.entity.core import static_entity_manager
from core.types import Time
from queue_simulator.queue_components.experiments import SimulationExperiment
from queue_simulator.queue_components.server import ServerProperty
from queue_simulator.queue_components.shared.models.node_property import NodeProperty
from queue_simulator.queue_components.shared.nodes import NodeType
from queue_simulator.queue_components.source import SourceProperty


class Prototype10Test(unittest.TestCase):
    vectors = {
        "test_1": {
            "time": Time(60 * 10),  # 10 minutes
            "source1": {
                "entities_per_arrival": {
                    "propertyName": SourceProperty.ENTITIES_PER_ARRIVAL,
                    "propertyValue": "1",
                    "propertyType": "EXPRESSION",
                    "propertyCategory": "GENERIC",
                },
                "inter_arrival_time": {
                    "propertyName": SourceProperty.INTER_ARRIVAL_TIME,
                    "propertyValue": "10",
                    "propertyType": "EXPRESSION",
                    "propertyCategory": "GENERIC",
                    "unit": "Seconds"
                }
            },
            "server1": {
                "processing_time": {
                    "propertyName": ServerProperty.PROCESSING_TIME,
                    "propertyValue": "2",
                    "propertyType": "EXPRESSION",
                    "propertyCategory": "GENERIC",
                    "unit": "Minutes"
                },
                "initial_capacity": {
                    "propertyName": ServerProperty.INITIAL_CAPACITY,
                    "propertyValue": "1000",
                    "propertyType": "NUMBER",
                    "propertyCategory": "GENERIC",
                    "unit": "Minutes"
                }
            }
        }

    }

    def setUp(self) -> None:
        self.experiment = SimulationExperiment()

    def tearDown(self) -> None:
        static_entity_manager._saved_names = set()

    def _create_label(self, expression: str):
        label = self.experiment.add_label()
        return self.experiment.edit_label(label.get_id(),
                                          NodeProperty("Expression", expression, 'EXPRESSION',
                                                       'GENERIC', None))

    def test_validation_1(self):
        test = 'test_1'
        time = self.vectors[test]['time']
        source = self.experiment.add_node(NodeType.SOURCE)
        server = self.experiment.add_node(NodeType.SERVER)
        sink = self.experiment.add_node(NodeType.SINK)
        self.experiment.add_path(source.get_id(), server.get_id())
        self.experiment.add_path(server.get_id(), sink.get_id())

        self.experiment.edit_property(source.get_id(),
                                      NodeProperty.deserialize(self.vectors[test]["source1"]["entities_per_arrival"]))

        self.experiment.edit_property(source.get_id(),
                                      NodeProperty.deserialize(self.vectors[test]["source1"]["inter_arrival_time"]))

        self.experiment.edit_property(server.get_id(),
                                      NodeProperty.deserialize(self.vectors[test]["server1"]["processing_time"]))

        self.experiment.edit_property(server.get_id(),
                                      NodeProperty.deserialize(self.vectors[test]["server1"]["initial_capacity"]))

        source_label_out = self._create_label("Source1.OutputBuffer.NumberEntered")

        server_label_in = self._create_label("Server1.InputBuffer.NumberEntered")
        server_label_out = self._create_label("Server1.OutputBuffer.NumberEntered")

        sink_label_in = self._create_label("Sink1.InputBuffer.NumberEntered")

        self.experiment.start_simulation(stop_time=time)
        self.experiment.simulation_control.wait()
        print([str(source_label_out), str(server_label_in), str(server_label_out), str(sink_label_in)])

if __name__ == '__main__':
    unittest.main()
