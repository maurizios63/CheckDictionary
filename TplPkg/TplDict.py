import logging


class TplDictC (dict):

    # Name of default key
    __default_key__ = '__default__'
    __logging_level = logging.INFO

    def __init__(self, *args, **kwargs):
        """
        Init method
        set type for each entry
        :param init_dict: Initialization dictionary to define types
        """
        self.is_default = False
        self.logger_name = kwargs.get('__name__','Main ')
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(TplDictC.__logging_level)
        super(TplDictC, self).__init__(*args, **kwargs)
        self.hidden_key_l = [TplDictC.__default_key__, '__name__']
        # Create a sub-dictionary containing type-keys
        self.type_dict = {key: type(value) for (key, value) in super(TplDictC, self).items()}
        # Initialize the set of keys that have default values
        self.default_key_set = self.get_keys
        self.has_default_type = self.get(TplDictC.__default_key__) is not None
        # Massage the dictionary and change all entries of type dict with type TplDict
        # Leave behind __default since if it is a dictionary we should use it to create a TpcDict
        #  at the time we had an objectz
        # dict_key_l = [key for key in super(TplDictC, self).keys() if isinstance(self[key], dict)]
        dict_key_l = [key for key in self.get_keys if isinstance(self[key], dict)]
        for key in dict_key_l:
            sub_dict = TplDictC(self[key], __name__="%s -> sub-key %s" %(self.logger_name, key))
            super(TplDictC, self).__setitem__(key, sub_dict)
            x = 1
            # self[key] = TplDictC(self[key])
        self.logger.debug("Init. done")

    def __setitem__(self, key, value):
        """
        Over-ride of set method:
            my_dict[key] = value
        Checks entries validity & then placed value into dictionary
        :param key:
        :param value:
        :return:
        """
        if self.check_tuple(key, value):
            if isinstance(value, dict):
                if self.is_default:
                    # We need to create instance
                    sub_dict = TplDictC(self[TplDictC.__default_key__],__name__="%s -> sub-key %s" %(self.logger_name, key))
                    super(TplDictC, self).__setitem__(key, sub_dict)
                    # self[key] = self[TplDictC.__default_key__]
                try:
                    self[key].update(value)
                except KeyError:
                    x = 1
                x = 1
                #super(TplDictC, self).__setitem__(key, TplDictC(value))
            else:
                super(TplDictC, self).__setitem__(key, value)
            if not self.is_default:
                try:
                    # Removed object from list
                    self.default_key_set.remove(key)
                except ValueError:
                    # If element is not present it means that has already been updated
                    self.logger.warning("Value of key %s is super-seeded" % key)

    def __iter__(self):
        return iter(self.get_keys)

    def keys(self):
        """
        Over-ride default dict values method
        :return: all keys except the 'hidden' key : __default
        """
        return self.get_keys

    def values(self):
        """
        Over-ride default dict values method
        :return: all key-values except the ones of 'hidden' keys : __default
        """
        return [self[key] for key in self.get_keys]

    def itervalues(self):
        """
        Over-ride default dict values method
        :return: all key-values except the ones of 'hidden' keys : __default
        """
        return (self[key] for key in self.get_keys)

    def update(self, *args, **kwargs):
        """
        Over-rides update method with a check of tuples
        :return:
        """
        # Process args
        new_dict = {}  # Initialize new_dict
        len_args = len(args)
        if len_args > 1:
            # As in default update method only 1 positional argument is allowed
            raise TypeError('update expected at most 1 arguments, got %d' % len_args)
        elif len_args == 1:
            # A dictionary has been specified as positional argument
            new_dict = args[0]
        new_dict.update(kwargs)  # Update dictionary with positional arguments
        for (key, value) in new_dict.items():
            # Check for invalid keys
            self.__setitem__(key, value)
            # super(TplDictC, self).__setitem__(key, value)
        self.logger.debug("Update done")

    @property
    def get_keys(self):
        """
        Procedure to return keys except the hidden ones
        :return:
        """
        return [key for key in super(TplDictC, self).keys() if key not in self.hidden_key_l]

    def check_tuple(self, key, value):
        """
        Verify if key, value tuple is valid
        :param key:
        :param value:
        :return: True if valid
        """
        # Check in standard keys
        self.is_default = False
        if key in self.get_keys:
            ref_type = self.type_dict[key]
        elif self.has_default_type:
            # Otherwise use default type if defined
            ref_type = self.type_dict[TplDictC.__default_key__]
            self.is_default = True  # Set the flag is_default to for dict update
        else:
            # Error out
            self.logger.error("Invalid key >%s<" % key)
            return False
        # Now check if type matches
        if type(value) is not ref_type:
            self.logger.error("Invalid type %s for key >%s<: expected %s" % (type(value), key, ref_type))
            return False
        else:
            return True

    def __repr__(self):
        """
        Over-rise default representation omitting hidden keys
        :return:
        """
        return {x: self[x] for x in self.get_keys}.__repr__()
