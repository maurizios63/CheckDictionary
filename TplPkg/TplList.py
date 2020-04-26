import logging
from . import TplDictC


class TplList(list):
    # Extract from abstract key
    # Name of default key
    __default_key__ = '__default__'
    __logging_level = logging.INFO

    def __init__(self, *args, **kwargs):
        # Set logger
        self.logger_name = kwargs.get('__name__', 'Main ')
        self.logger = logging.getLogger(self.logger_name)
        self.ref_list = kwargs.get('ref_list', [])
        self._inner_list = args[0]
        #super(TplList, self).__init__(*args)

        # Check that reference list is a list
        if type(self.ref_list) is not list:
            raise ValueError("ref_name argument should be a list")
        self.type_l = [type(x) for x in self.ref_list]
        self.ref_dict = None
        # Check for ref_dict
        self.ref_dict_l = [x for x in self.ref_list if isinstance(x, dict)]
        if len(self.ref_dict_l) > 1:
            raise ValueError("ref_dict containt at most 1 dictionary")
        elif len(self.ref_dict_l) == 1:
            self.ref_dict = self.ref_dict_l[0]
        len_args = len(args)
        if len_args > 1:
            # As in default update method only 1 positional argument is allowed
            raise TypeError('update expected at most 1 arguments, got %d' % len_args)
        elif len_args == 1:
            # A dictionary has been specified as positional argument
            for value in args[0]:
                add_value = self.check_element(value)
                if add_value is not None:
                    super().append(add_value)  # Use parent method to avoid calling chelc method again
        self.logger.debug("Done")

    @property
    def valid_types(self):
        """
        Return valid types as string
        :return: string
        """
        return ','.join([str(x) for x in self.type_l])

    def check_element(self, value):
        """
        Check if element is valid and in case append to list
        :param value:  Value to be check
        :return: value (if valid) otherwise None
        """
        if type(value) not in self.type_l:
            self.logger.error("Invalid type %s for value >%s<: expected %s" %
                              (type(value), value, self.valid_types))
            return None
        elif isinstance(value, dict):
            # In case of a dictionary we create a dictionary object
            new_dict = TplDictC(self.ref_dict)
            new_dict.update(value)
            return new_dict
        else:
            return value

    def __len__(self):
        return len(self._inner_list)

    def insert(self, index, value):
        add_value = self.check_element(value)
        if add_value is not None:
            super().insert(index, add_value)

    def __setitem__(self, index, value):
        """
        Standard method: delete item
        :param index: item to be deleted
        :return: None
        """
        add_value = self.check_element(value)
        if add_value is not None:
            super().__setitem__(index, add_value)

    def append(self, value):
        add_value = self.check_element(value)
        if add_value is not None:
            super().append(add_value)  # Use parent method to avoid calling chelc method again

