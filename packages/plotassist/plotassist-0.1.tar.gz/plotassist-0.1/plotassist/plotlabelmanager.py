# plotlabelmanager.py

# Classes to help with labeling Matplotlib plots.


class PlotLabel:
    """
    A class to represent a label for a Matplotlib plot.

    Attributes:
    ----------
    key : object
        The key associated with the PlotLabel object.
    text : str
        The text for the PlotLabel object.
    plt_args : dict
        A dictionary of plotting arguments for the PlotLabel object.

    Methods:
    -------
    __init__(self, key: object, text: str, plt_args: dict)
        Initializes the PlotLabel object with the given key, text, and plotting arguments.

    get_key(self) -> object
        Returns the key associated with the PlotLabel object.

    get_text(self) -> str
        Returns the text for the PlotLabel object.

    get_plt_args(self) -> dict
        Returns the dictionary of plotting arguments for the PlotLabel object.

    __repr__(self)
        Returns a string representation of the PlotLabel object.
    """

    def __init__(self, key: object, text: str, plt_args: dict):
        """
        Initializes the PlotLabel object with the given key, text, and plotting arguments.

        Parameters:
        ----------
        key : object
            The key associated with the PlotLabel object.
        text : str
            The text for the PlotLabel object.
        plt_args : dict
            A dictionary of plotting arguments for the PlotLabel object.

        Raises:
        ------
        ValueError
            If plt_args is None or not a dictionary, or if text is not a string.
        """
        # ensure that plt_args is at least an empty dict
        if plt_args is None:
            raise ValueError("plt_args cannot be None")
        if not isinstance(plt_args, dict):
            raise ValueError("plt_args must be a dict")

        # ensure text is a string
        if not isinstance(text, str):
            raise ValueError("text must be a string")

        # save data
        self.key = key
        self.text = text
        self.plt_args = plt_args

    def get_key(self) -> object:
        """
        Returns the key associated with the PlotLabel object.

        Returns:
        -------
        object
            The key associated with the PlotLabel object.
        """
        return self.key

    def get_text(self) -> str:
        """
        Returns the text for the PlotLabel object.

        Returns:
        -------
        str
            The text for the PlotLabel object.
        """
        return self.text

    def get_plt_args(self) -> dict:
        """
        Returns the dictionary of plotting arguments for the PlotLabel object.

        Returns:
        -------
        dict
            The dictionary of plotting arguments for the PlotLabel object.
        """
        return self.plt_args

    def __repr__(self):
        return f"PlotLabel(key={self.key}, text='{self.text}', plt_args={self.plt_args})"



class PlotLabelManager:
    """
    A class to manage PlotLabel objects for labeling Matplotlib plots.

    Attributes:
    ----------
    labels : dict
        A dictionary to hold PlotLabel objects.
    access : dict
        A dictionary to track access to PlotLabel objects.
    arg_map : dict[str, list]
        A dictionary mapping keys to lists of arguments for PlotLabel objects.

    Methods:
    -------
    __init__(self, args_map_dict: dict[str, list])
        Initializes the PlotLabelManager with a dictionary of argument mappings.

    get_plot_label(self, key: object) -> PlotLabel
        Returns the PlotLabel object associated with the given key.

    key_exists(self, key: object) -> bool
        Checks if a key exists in the labels dictionary.
    """

    def __init__(self, args_map_dict: dict[str, list]):
        """
        Initializes the PlotLabelManager with a dictionary of argument mappings.

        Parameters:
        ----------
        args_map_dict : dict[str, list]
            A dictionary mapping keys to lists of arguments for PlotLabel objects.

        Raises:
        ------
        ValueError
            If the lists in args_map_dict have inconsistent lengths.
        """
        # define a dict to hold PlotLabel objects and access booleans
        self.labels = {}
        self.access = {}

        # store the argument map with lists reversed for popping
        self.arg_map = {k:v[::-1] for k, v in args_map_dict.items()}

        # check for inconsistent list lengths
        list_lens = set(len(v) for v in self.arg_map.values())
        if len(list_lens) > 1:
            # get the shortest list
            min_len = min(list_lens)

            # print warning
            print(f"Warning: not all lists in arg_map are the same length. Shortest list has {min_len} elements.")


    def get_plot_label(self, key: object) -> PlotLabel:
        """
        Returns the PlotLabel object associated with the given key.

        Parameters:
        ----------
        key : object
            The key associated with the desired PlotLabel object.

        Returns:
        -------
        PlotLabel
            The PlotLabel object associated with the given key.

        Raises:
        ------
        ValueError
            If the key does not exist in the labels dictionary.
        """
        # check if key exists
        if not self.key_exists(key):
            raise ValueError(f"Key '{key}' not found")

        return self.labels[key]


    def key_exists(self, key: object) -> bool:
        """
        Checks if a key exists in the labels dictionary.

        Parameters:
        ----------
        key : object
            The key to check for existence in the labels dictionary.

        Returns:
        -------
        bool
            True if the key exists, False otherwise.
        """
        return key in self.labels


    def add(self, key: object, text: str, plt_args: dict = None) -> None:
        """
        Adds a new PlotLabel object to the labels dictionary.

        Parameters:
        ----------
        key : object
            The key associated with the new PlotLabel object.
        text : str
            The text for the new PlotLabel object.
        plt_args : dict, optional
            A dictionary of plotting arguments for the new PlotLabel object. If None, arguments are extracted from the arg_map.

        Raises:
        ------
        ValueError
            If the key already exists in the labels dictionary.
        """
        # check if key is already in list
        if self.key_exists(key):
            raise ValueError(f"Key '{key}' already exists")

        # if no plt_args are supplied, extract them from the arg_map
        if plt_args is None:
            # replace plt_args with an empty dict
            plt_args = {}

            # iterate over each key:list pair of the arg_map
            for arg_key, arg_list in self.arg_map.items():
                # check that arg_list is not empty
                if len(arg_list) == 0:
                    raise IndexError(f"arg_list for '{arg_key}' has been depleted of unique values")

                # the key of arg_key is the argument key in matplotlib.plt
                plt_args[arg_key] = arg_list.pop()

        # create a new PlotLabel object and append
        plot_label = PlotLabel(key, text, plt_args)
        self.labels[plot_label.get_key()] = plot_label
        self.access[plot_label.get_key()] = False


    def try_add(self, key: object, text: str, plt_args: dict = None) -> None:
        """
        Tries to add a new PlotLabel object to the labels dictionary if the key does not already exist.

        Parameters:
        ----------
        key : object
            The key associated with the new PlotLabel object.
        text : str
            The text for the new PlotLabel object.
        plt_args : dict, optional
            A dictionary of plotting arguments for the new PlotLabel object. If None, arguments are extracted from the arg_map.
        """
        # check if key is not already in list
        if not self.key_exists(key):
            self.add(key=key, text=text, plt_args=plt_args)


    def get_args(self, key: object) -> dict:
        """
        Returns the plotting arguments for the PlotLabel object associated with the given key.

        Parameters:
        ----------
        key : object
            The key associated with the desired PlotLabel object.

        Returns:
        -------
        dict
            A dictionary of plotting arguments for the PlotLabel object, including the 'label' key.
        """
        # prepare the return dict
        plot_label = self.get_plot_label(key)
        return_dict = plot_label.get_plt_args().copy()
        return_dict['label'] = plot_label.get_text()

        # deduplicate the label entry for plotting
        if self.access[key]:
            return_dict['label'] = None
        else:
            self.access[key] = True

        return return_dict


    def __repr__(self):
        # compose the repr string out of repr strings from contained plot labels in a list
        head = "PlotLabelManager:\n - "
        labels = "\n - ".join([f"{plot_label}" for plot_label in self.labels.values()])

        return_str = head + labels
        return return_str
