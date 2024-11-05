from .config import MachineConfig
from transitions.extensions import HierarchicalGraphMachine as Machine
from transitions.extensions.states import add_state_features, Timeout
from transitions.core import listify, EventData, Event
from pigeon import Pigeon
from pigeon.utils import setup_logging, call_with_correct_args


@add_state_features(Timeout)
class BaseMachine(Machine):
    _model = []

    def __init__(
        self,
        states=None,
        transitions=None,
        on_enter=None,
        before_state_change=None,
        after_state_change=None,
        prepare_event=None,
        finalize_event=None,
        on_exception=None,
        on_final=None,
        **kwargs,
    ):
        """The standard transitions Machine constructor with the folowing changes:

        * The model is disabled.
        * An on_enter callback is created on the machine and transformed using _get_callables and _get_callable.
        * The before_state_change, after_state_change, prepare_event, finalize_event, on_exception, and on_final
            callbacks are transformed using _get_callables and _get_callable.
        """
        self.parent = None
        self.state_name = None
        self._children = {}
        self._on_enter = self._get_callables(on_enter)
        super().__init__(
            states=states,
            transitions=transitions,
            model=self._model,
            before_state_change=self._get_callables(before_state_change),
            after_state_change=self._get_callables(after_state_change),
            prepare_event=self._get_callables(prepare_event),
            finalize_event=self._get_callables(finalize_event),
            on_exception=self._get_callables(on_exception),
            on_final=self._get_callables(on_final),
            auto_transitions=False,
            **kwargs,
        )

    @classmethod
    def init_child(cls, name, config, *args, **kwargs):
        """This is a helper routine for propogating configuration to child machines."""
        if isinstance(config, MachineConfig) and hasattr(config, name):
            kwargs["config"] = getattr(config, name)
            kwargs.update(getattr(config, name).config)
        return cls(*args, **kwargs)

    def _create_state(
        self, *args, on_enter=None, on_exit=None, on_timeout=None, **kwargs
    ):
        """Transform callbacks using _get_callables"""
        return super()._create_state(
            *args,
            on_enter=self._get_callables(on_enter),
            on_exit=self._get_callables(on_exit),
            on_timeout=self._get_callables(on_timeout),
            **kwargs,
        )

    def add_transition(
        self,
        *args,
        conditions=None,
        unless=None,
        before=None,
        after=None,
        prepare=None,
        **kwargs,
    ):
        """Transform callbacks using _get_callables"""
        return super().add_transition(
            *args,
            conditions=self._get_callables(conditions),
            unless=self._get_callables(unless),
            before=self._get_callables(before),
            after=self._get_callables(after),
            prepare=self._get_callables(prepare),
            **kwargs,
        )

    def _get_callable(self, func):
        """Get a class member function of the same name as the input if available.
        If the class member is not a function, create a lambda function which
        returns the current value of the class member variable. If the input is
        a variable, return a lambda function which returns the current value of
        the variable."""
        if isinstance(func, str):
            if hasattr(self, func):
                tmp = getattr(self, func)
                if callable(tmp):
                    return tmp
                else:
                    geter = lambda: getattr(self, func)
                    # Setting the __name__ attribute shows the function name on the graph
                    geter.__name__ = func
                    return geter
            else:
                return func
        if not callable(func):
            return lambda: func
        return func

    def _get_callables(self, funcs):
        """Returns a transformed list of callbacks with string entries substituted
        for class member functions when available."""
        if funcs is None:
            return []
        return [self._get_callable(func) for func in listify(funcs)]

    def _add_machine_states(self, state, remap):
        """This method is overridden to build the parent, child relationships
        between each machine in the hierarchy."""
        state.parent = self
        state.state_name = self.get_global_name()
        self._children[self.get_global_name()] = state
        super()._add_machine_states(state, remap)

    def _add_dict_state(self, state, *args, **kwargs):
        """This method is overridden to add the child machine's on_enter
        callback(s) to the parent state's on_enter callback."""
        state["on_enter"] = listify(state.get("on_enter"))
        if "children" in state and isinstance(state["children"], BaseMachine):
            state["on_enter"] += state["children"]._on_enter
        return super()._add_dict_state(state, *args, **kwargs)

    def _remap_state(self, state, remap):
        """This function overrides the normal _remap_state method to also remove
        the remaped state so it does not appear in the diagram. Additionally, any
        on_enter callbacks of the remapped start are move to the after callbacks of
        the transition."""
        remapped_transitions = super()._remap_state(state, remap)
        for orig, new in remap.items():
            on_enter = self.states[orig].on_enter
            for transition in remapped_transitions:
                if transition["dest"] == new:
                    transition["before"] += on_enter
        for old_state in remap.keys():
            del self.states[old_state]
        return remapped_transitions

    def message_callback(self):
        """This message callback can be overridden with the desired functionality
        for the machine. All machines in the hierarchy of active states will have
        this method called, starting at the leaf."""
        pass

    @property
    def root(self):
        """Traverse the tree of hierarchical machines to the root and return it."""
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    @property
    def client(self):
        """Returns the Pigeon client, or None, if the machine is not part of the
        current state."""
        if self._current_machine():
            return self.root._client
        return None

    def get_state_path(self, join=True):
        """Returns the hierarchical state that leads to this machine.

        If join is False, returns a list of hierarchical states which lead to
            this machine."""
        parent = self
        states = []
        while parent.parent is not None:
            states.insert(0, parent.state_name)
            parent = parent.parent
        if join:
            return self.separator.join(states)
        return states

    def get_machine_state(self):
        """Returns the current state of this machine, or None, if the current
        state is not a state in this machine, or a substate."""
        state_path = self.get_state_path(join=False)
        state = self.state.split(self.separator)
        if any(
            [
                state_comp != state_path_comp
                for state_comp, state_path_comp in zip(state, state_path)
            ]
        ):
            return None
        return state[len(state_path)]

    def _current_machine(self):
        """Returns True if the current state is a state of this machine, or a substate."""
        return self.get_machine_state() is not None

    def current_machine(self):
        """Returns True if the current state is a state of this machine strictly."""
        if not self._current_machine():
            return False
        state = self.state.split(self.separator)
        state_path = self.get_state_path(join=False)
        return len(state_path) + 1 == len(state)

    def __getattr__(self, name):
        """If a class attribute is not available in this class, try to get it
        from the root class."""
        if self.parent is None:
            return super().__getattr__(name)
        return getattr(self.root, name)


class RootMachine(BaseMachine):
    _model = Machine.self_literal

    def __init__(self, logger=None, **kwargs):
        """This constructor builds on the BaseMachine constructor adding the following:

        * The state machine model is the class instance.
        * Auto transitions are disabled.
        * State attributes (callbacks etc.), and transition conditions and callbacks are
            configured to be displayed on the graph.
        * Active and previous states are styled the same as the inactive states on the graph.
        * A logger is created if not provided.
        """
        self._client = None
        self.parent = None
        self._collected = {}
        self.style_attributes["node"]["active"] = self.style_attributes["node"][
            "inactive"
        ]
        self.style_attributes["node"]["previous"] = self.style_attributes["node"][
            "inactive"
        ]
        kwargs["after_state_change"] = (
            listify(kwargs["after_state_change"])
            if "after_state_change" in kwargs
            else []
        )
        kwargs["after_state_change"].append(self._log_state_change)
        super().__init__(
            show_conditions=True,
            show_state_attributes=True,
            **kwargs,
        )
        self._logger = logger if logger is not None else setup_logging(__name__)

    def _init_graphviz_engine(self, graph_engine):
        """This method takes the existing graph class selected based on what
        graph engine and creates and returns a subclass."""

        class Graph(super()._init_graphviz_engine(graph_engine)):
            def _transition_label(self, trans):
                """This method is overridden to add displaying of the before and
                after transition callbacks on the graph."""
                label = super()._transition_label(trans)
                if "before" in trans and trans["before"]:
                    label += r"\lbefore: {}".format(", ".join(trans["before"]))
                if "after" in trans and trans["after"]:
                    label += r"\lafter: {}".format(", ".join(trans["after"]))
                return label

        return Graph

    def add_client(
        self, service=None, host="127.0.0.1", port=61616, username=None, password=None
    ):
        """This method adds a Pigeon client to the class, and subscribes to all
        known messages."""
        self._client = Pigeon(
            service if service is not None else self.__class__.__name__,
            host=host,
            port=port,
        )
        self._client.connect(username=username, password=password)
        self._client.subscribe_all(self._message_callback)

    def save_graph(self, path):
        """This method saves a graph of the hierarchical state machine to the
        provided path."""
        extension = path.split(".")[-1].lower()
        self.get_graph().render(format=extension, cleanup=True, outfile=path)

    def _log_state_change(self):
        self._logger.info(f"Transitioned to state: {self.state}")

    def _get_machine(self, state):
        """This method returns the machine instance which a given state is part of."""
        child = self
        for state in state.split(self.separator)[:-1]:
            child = child._children[state]
        return child

    def _get_current_machine(self):
        """This method returns the machine instance which the current state is part of."""
        return self._get_machine(self.state)

    def _get_current_machines(self):
        """This generator first yields the full hierarchical state of the current
        machine then continues yielding states descending to the root machine."""
        state_list = self.state.split(self.separator)
        yield self._get_current_machine()
        for i in range(1, len(state_list)):
            yield self._get_machine(self.separator.join(state_list[:-i]))

    def _message_callback(self, msg, topic, *args, **kwargs):
        """This method is the main callback for Pigeon messages. It stores the
        most recent message on each topic, and it takes the message and calls
        the message_callback function in each machine, starting at the leaf,
        and traversing to the root."""
        self._collect(topic, msg)
        for machine in self._get_current_machines():
            try:
                call_with_correct_args(
                    machine.message_callback, msg, topic, *args, **kwargs
                )
            except Exception as e:
                self._logger.warning(
                    f"Callback for a message on topic '{topic}' with data '{msg}' resulted in an exception:",
                    exc_info=True,
                )

    def _collect(self, topic, msg):
        """This method stores the most recent message recieved on each topic."""
        self._collected[topic] = msg

    def get_collected(self, topic):
        """This function returns the most recent message recieved on a given topic."""
        self._client._ensure_topic_exists(topic)
        return self._collected.get(topic, None)

    def _get_initial_states(self):
        """This method returns the set of initial states of the hierarchical state machine."""
        states = [self.states[self.initial]]
        while len(states[-1].states):
            states.append(states[-1].states[states[-1].initial])
        return states

    def _start(self):
        """This method can be called at the beginning of execution of the state
        machine. It runs the on_enter callback of each of the machines that are
        part of the initial state."""
        for state in self._get_initial_states():
            state.enter(
                EventData(state, Event("_start", self), self, self, args=[], kwargs={})
            )

    def _run(self):
        """This method runs the _start routine, then enters an infinte loop."""
        self._start()
        while True:
            pass
