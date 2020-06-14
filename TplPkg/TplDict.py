import logging
# import sys
import re

from collections import OrderedDict


class TplDictC (OrderedDict):

    # Name of default key
    _log_name = 'TplDictC'
    _ERROR = 2
    _WARNING = 1
    _OK = 0
    _status = _OK

    _logging_level = logging.INFO
    _ref_dict = {}  # Reference dictionary: initially empty
    _mandatory_keys = []  # List of mandatory keys : initially empty

    def __init__(self, tgt_dict, ref_dict, logger_name="TplDictC" ):
        """
        Init method

        """
        # Set logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(TplDictC._logging_level)
        # Check if _ref_dict key has been specified
        self._ref_dict = ref_dict
        self._tgt_dict = { }
        for key, value in tgt_dict.items():
            ref_key = self.check_tuple(key, value)
            if ref_key is not None:
                if isinstance(value, dict):
                    self._tgt_dict[key] = TplDictC(tgt_dict=self._tgt_dict[key], ref_dict=value)
                else:
                    self._tgt_dict[key] = value

    def check_tuple(self, key, value):
        """
        Verify if key, value tuple is valid
        :param key:
        :param value:
        :return: reference key if found, None otherwise
        """
        # Check in standard keys
        ref_key = self.get_ref_key(key)
        if ref_key is not None:
            ref_type = type(self._ref_dict[ref_key])
            # Now check if type matches
            if type(value) is not ref_type:
                self.logger.error("Invalid type %s for key >%s<: expected %s" % (type(value), key, ref_type))
                self._status = TplDictC._ERROR
                return None
            else:
                return ref_key

    def get_ref_key(self, key):
        """
        Return key from reference dictionary
        :param key: Key in actual dictionary
        :return: key in reference dictionary (maybe a regex), None if not found
        """
        try:
            # The dictionary is ordered so we pick the 1st matching
            return [ref_key for ref_key in self._ref_dict.keys() if re.findall(ref_key, key)][0]
        except IndexError:
            self.logger.error("Invalid key : %s" % key)
            self._status = TplDictC._ERROR
            return None

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
                    sub_dict = TplDictC(self[TplDictC.__default_key__],
                                        __name__="%s -> sub-key %s" % (self.logger_name, key))
                    super(TplDictC, self).__setitem__(key, sub_dict)
                self[key].update(value)

            else:
                super(TplDictC, self).__setitem__(key, value)

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
        return [key for key in super(TplDictC, self).keys() if not key.startswith('_')]

    def __repr__(self):
        """
        Over-rise default representation omitting hidden keys
        :return:
        """
        # return {x: self[x] for x in self.get_keys}.__repr__()
        return self._tgt_dict.__repr__()

    @property
    def get_status(self):
        """
        Return test status
        :return: int
        """
        self.logger.debug("Test status is %d" % self._status)
        return self._status

    def get(self, key, value=None):
        """
        Over-riding dictionary get method
        :param key: key to be got
        :param value: defualt value to be returned if key is missing
        :return: corresponding key of internal target dictionary
        """
        return self._tgt_dict.get(key, value)