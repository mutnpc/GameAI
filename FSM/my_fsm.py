class StateMachine:
    def __init__(self, cfg, states, events_handler, actions_handler):
        # config information for an instance
        self.cfg = cfg
        # define the states and the initial state
        self.states = [s.lower() for s in states]
        self.state = self.states[0]
        # process the inputs according to current state
        self.events = dict()
        # actions according to current transfer 
        self.actions = {state: dict() for state in self.states}
        # cached data for temporary use
        self.records = dict()
        # add events and actions
        for i, state in enumerate(self.states):
            self._add_event(state, events_handler[i])
            for j, n_state in enumerate(self.states):
                self._add_action(state, n_state, actions_handler[i][j])

    def _add_event(self, state, handler):
        self.events[state] = handler

    def _add_action(self, cur_state, next_state, handler):
        self.actions[cur_state][next_state] = handler

    def run(self, inputs):
        # decide the state-transfer according to the inputs
        new_state, outputs = self.events[self.state](inputs, self.states, self.records, self.cfg)
        # do the actions related with the transfer 
        self.actions[self.state][new_state](outputs, self.records, self.cfg)
        # do the state transfer
        self.state = new_state
        return new_state

    def reset(self):
        self.state = self.states[0]
        self.records = dict()
        return

# handlers for events and actions, event_X and action_XX are all specific functions
events_handlers = [event_A, event_B]
actions_handlers = [[action_AA, action_AB],
                    [action_BA, action_BB]]

# define an instance of StateMachine
state_machine = StateMachine(cfg, states, events_handlers, actions_handlers)


class StateGeneral(StateMachine):
    def __init__(self, cfg, states):
        super(StateGeneral, self).__init__(cfg, states, events_handler, actions_handler)
        self.sub_state_machines = dict()

    def add_sub_fsm(self, name, fsm):
        self.sub_state_machines[name] = fsm

    def run(self, inputs):
        new_state, outputs = self.events[self.state](inputs, self.states, self.records, self.cfg)
        # operate the sub_state_machines in actions
        self.actions[self.state][new_state](outputs, self.records, self.cfg, \
                 self.sub_state_machines)
        self.state = new_state
        return new_state

    def reset(self):
        self.state = self.states[0]
        self.records = dict()
        for _, sub_fsm in self.sub_state_machines.items():
            sub_fsm.reset()
        return


def main():
    # test the StateMachine
    state_machine.run(inputs)
    

if __init__ == '__main__':
    main()

    

