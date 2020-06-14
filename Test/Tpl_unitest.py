import unittest
from _collections import OrderedDict
from TplPkg import TplDictC


class MyTestCase(unittest.TestCase):

    def check_dictionary(self, tgt_dict, tgt_tpl_dict, faulty_keys=[]):
        for key in tgt_dict.keys():
            if key in faulty_keys:
                self.assertEqual(tgt_tpl_dict.get('a_int', '__'), '__')
            else:
                self.assertEqual(tgt_dict[key], tgt_tpl_dict.get(key, '__'))

    def test_flat_dict_ok(self):
        """
        Check flat dictionary without usage of regexp
        :return:
        """
        print("----------------")
        print(self._testMethodName)
        print(" " + self.shortDescription())

        ref_dict = OrderedDict(a=1, b='ss', c=3.4)
        tgt_dict = dict(a=5, b='yy', c=5.6)
        tgt_tpl_dict = TplDictC(tgt_dict=tgt_dict, ref_dict=ref_dict)
        status = tgt_tpl_dict.get_status
        print(tgt_tpl_dict)
#        self.assertEqual(tgt_tpl_dict, tgt_dict.__repr__())
        self.check_dictionary( tgt_dict, tgt_tpl_dict)
        self.assertEqual(status, TplDictC._OK)

    def test_re_dict_ok(self):
        """
        Check flat directory using regular expressions
        :return:
        """
        print("----------------")
        print(self._testMethodName)
        print(" " + self.shortDescription())

        ref_dict = OrderedDict({'.*_int': 1, '.*_str': 'ss', '.*_float': 3.4})
        tgt_dict = dict(a_int=5, b_str='yy', c_float=5.6)
        tgt_tpl_dict = TplDictC(tgt_dict=tgt_dict, ref_dict=ref_dict)
        status = tgt_tpl_dict.get_status
        print(tgt_tpl_dict)
#        self.assertEqual(tgt_tpl_dict, tgt_dict.__repr__())
        self.check_dictionary( tgt_dict, tgt_tpl_dict)

        self.assertEqual(status, TplDictC._OK)

    def test_re_dict_fail(self):
        """
        Flat directory: force a failure on 1st element
        :return:
        """
        print("----------------")
        print(self._testMethodName)
        print(" ", self.shortDescription())
        ref_dict = OrderedDict({'.*_int': 1, '.*_str': 'ss', '.*_float': 3.4})
        tgt_dict = dict(a_int=5.4, b_str='yy', c_float=5.6)
        tgt_tpl_dict = TplDictC(tgt_dict=tgt_dict, ref_dict=ref_dict)
        status = tgt_tpl_dict.get_status
        print("tgt_tpl_dict:", tgt_tpl_dict)
        #        self.assertEqual(tgt_tpl_dict, tgt_dict.__repr__())
        self.check_dictionary( tgt_dict, tgt_tpl_dict, faulty_keys=['a_int'])

        # self.assertEqual(tgt_tpl_dict.get('a_int', '__'), '__')
        # self.assertEqual(tgt_dict['b_str'], tgt_tpl_dict.get('b_str', '__'))
        # self.assertEqual(tgt_dict['c_float'], tgt_tpl_dict.get('c_float', '__'))


if __name__ == '__main__':
    unittest.main()
