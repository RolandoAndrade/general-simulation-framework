import unittest
from random import seed

from core.components.entity.properties.number_property import NumberProperty
from queue_simulator.buffer.buffers.output_buffer import OutputBuffer
from queue_simulator.buffer.core.buffer_policy import BufferPolicy
from queue_simulator.buffer.core.buffer_property import BufferProperty
from test.queue_simulator.buffer.mocks.mock_emitter import MockEmitter


class TestOutputBuffer(unittest.TestCase):
    buffer: OutputBuffer

    def setUp(self) -> None:
        self.buffer = OutputBuffer("Source")
        seed(42)

    def test_name(self):
        """Name should be <name>.OutputBuffer"""
        self.assertEqual("Source.OutputBuffer", self.buffer.getID(), "Error")

    def test_add_entity(self):
        """Should add entities to buffer"""
        self.buffer.add(MockEmitter())
        self.assertEqual(1, self.buffer.currentNumberOfEntities, "Error 0")
        self.buffer.add(MockEmitter(), 3)
        self.assertEqual(4, self.buffer.currentNumberOfEntities, "Error 1")

    def test_get_content(self):
        """Should retrieve the content"""
        # FIFO
        self.buffer.add(MockEmitter(), 5)
        ex = ["1", "2", "3", "4", "5"]
        re = [entity.getID() for entity in self.buffer.getContent()]
        self.assertEqual(ex, re, "Error 0")

        # LIFO
        self.buffer.policy = BufferPolicy.LIFO
        ex.reverse()
        re = [entity.getID() for entity in self.buffer.getContent()]
        self.assertEqual(ex, re, "Error 1")

        # RSM
        self.buffer.policy = BufferPolicy.RSM
        ex = ['4', '2', '3', '5', '1']
        re = [entity.getID() for entity in self.buffer.getContent()]
        self.assertEqual(ex, re, "Error 2")

    def test_pop_entity(self):
        """Should pop the entities in buffer"""
        self.buffer.add(MockEmitter(), 5)
        # ["1", "2", "3", "4", "5"]
        # FIFO
        re = self.buffer.pop()
        self.assertEqual('1', re.getID(), 'Error 0')

        # LIFO
        self.buffer.policy = BufferPolicy.LIFO
        re = self.buffer.pop()
        self.assertEqual('5', re.getID(), 'Error 1')

        # RSM
        self.buffer.policy = BufferPolicy.RSM
        re = self.buffer.pop()
        self.assertEqual('2', re.getID(), 'Error 2')

    def test_properties(self):
        """Should retrieve the properties of the buffer"""
        self.buffer.add(MockEmitter(), 3)
        self.buffer.pop()
        properties = self.buffer.getProperties()
        self.assertEqual(float('inf'), properties.get(BufferProperty.CAPACITY))
        self.assertEqual(BufferPolicy.FIFO, properties.get(BufferProperty.POLICY))
        self.assertEqual(3, properties.get(BufferProperty.NUMBER_ENTERED))

    def test_buffer_full(self):
        """Should be trunc the buffer and return
        the number of entities that cannot be saved"""
        self.buffer = OutputBuffer("Source", capacity=NumberProperty(5))
        re = self.buffer.add(MockEmitter(), 10)
        self.assertEqual(5, re)


if __name__ == '__main__':
    unittest.main()
