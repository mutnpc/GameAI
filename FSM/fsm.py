#pip install transitions

from transitions import Machine

class FSM(object):
    def __init__(self):
        self.sv = 0  # state variable of the model
        self.conditions = {  # each state
            'sA': 0,
            'sB': 3,
            'sC': 6,
            'sD': 0,
        }

    def poll(self):
        if self.sv >= self.conditions[self.state]:
            self.next_state()  # go to next state
        else:
            getattr(self, 'to_%s' % self.state)()  # enter current state again

    def on_enter(self):
        print('entered state %s' % self.state)

    def on_exit(self):
        print('exited state %s' % self.state)


def main():
    model = FSM()

    list_of_states = ['sA', 'sB', 'sC', 'sD']
    machine = Machine(model=model, states=list_of_states, initial='sA',
                    ordered_transitions=True, before_state_change='on_exit',
                    after_state_change='on_enter')

    for i in range(0, 10):
        print('iter is: ' + str(i) + " -model state is:" +  model.state)
        model.sv = i
        model.poll()


if __name__ == '__main__':
    main()