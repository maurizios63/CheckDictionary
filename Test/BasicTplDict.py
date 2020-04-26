from TplPkg import TplDictC
import logging
my_init_dict = {
    'class': 'xx',
    'date': {'year': 1900, 'month': 'Jan', 'day': 1},
    '__default__': 10,
    'student': {'__default__': {
            'Age': 4,
            'Marks': [10]
        }
    }
}

user_dict = {
    'class': '2a',
    'date': {'year': 2020, 'month': 'May', 'day': 30},
    'student': {
        'John': {'Age': 16, 'Marks': [8, 10, 5] },
        'Mary': {'Age': 17, 'Marks': [6]},
        'Frank': {'Age': 18, 'Marks':  [7, 4.2]},
    }
}


logging.basicConfig(level=logging.INFO)

my_dict_obj = TplDictC(my_init_dict)
logging.info(my_dict_obj)
logging.info('Keys : %s', '.'.join(my_dict_obj.keys()))
logging.info("----------")
my_dict_obj.update(user_dict)
logging.info(my_dict_obj)