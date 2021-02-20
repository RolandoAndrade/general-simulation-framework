class SimulationEngine:
    """Returns the simulation time at which the state was last computed"""

    def get_time(self):
        pass

    """First computes model's output function if this has not already been done, then 
    computes the model's next state and notifies listeners of these actions and finally
    tells the model to clean up objects created by its output function"""

    def compute_next_state(self):
        pass

    """Invokes the model's output function and inform to listeners of the consequent 
    output values; it does not change the state of the model"""

    def compute_output(self):
        pass
