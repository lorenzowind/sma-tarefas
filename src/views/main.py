from controllers.Persistance import Persistance
from controllers.Scheduler import Scheduler
from controllers.Simulation import Simulation

if __name__ == '__main__':
  option = None

  persistance = Persistance()

  numbers_to_generate = 100000
  scheduler = Scheduler(persistance.get_event_names(), numbers_to_generate)

  simulation = Simulation(persistance, scheduler)

  simulation.simulate_model()
