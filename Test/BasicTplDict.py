from TplPkg import TplDictC
import logging
my_init_dict = {

    'a': 123,
    'b': 123.45,
    'c': 'John Doe',
    'd': {'a': 1.5, 'b': 4},
     '__default__' : 10
}

user_dict = {

    'a': 143,
    'b': 445.5,
    'c': 'Mike Smith',
    'd': {'a': 3, 'b': 7}
}


logging.basicConfig(level=logging.INFO)

my_dict_obj = TplDictC(my_init_dict)
logging.info(my_dict_obj)
logging.info('Keys : %s', '.'.join(my_dict_obj.keys()))
logging.info("----------")
my_dict_obj.update(user_dict, d={'x':5}, f=7.1)
logging.info(my_dict_obj)
logging.info("----------")
my_dict_obj.update(b=65.13)
logging.info(my_dict_obj)
logging.info("----------")
my_dict_obj['a']=20
logging.info(my_dict_obj)
logging.info("----------")
my_dict_obj['a']=20.5
logging.info(my_dict_obj)


