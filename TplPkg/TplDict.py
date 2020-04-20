import logging


class TplDictC (dict):

    def __init__(self,init_dict={}):
        """
        Init method
        set type for each entry
        :param init_dict: Initialization dictionary to define types
        """
        super(TplDictC, self).__init__()
        self.logger = logging.getLogger('TplDictC')
        # Now process each keyboard entry for init. dictionary
        self.type_d = {key: type(value) for (key, value) in init_dict.items()}
        self.logger.info("Init. done")

    def update(self, user_dict, **kwargs):
        """
        Put the real value from the user dictionary (checking the types)
        :param user_dict:
        :return:
        """
        for (key, value) in user_dict.items():
            # Check for invalid keys
            if key not in self.type_d.keys():
                self.logger.error("Invalid key %s" % key)
            elif type(value) != self.type_d[key]:
                self.logger.error("Invalid type %s for values %s (key %s): expected %s" %
                                  (type(value), value, key, self.type_d[key]))
            else:
                super(TplDictC,self).__setitem__(key,value)
        self.logger.info("Update done")


