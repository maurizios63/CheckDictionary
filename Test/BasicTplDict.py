from TplPkg import TplDictC
import logging
my_init_dict = {

    'a': 123,
    'b': 123.45,
    'c': 'John Doe'
}

user_dict = {

    'a': 143,
    'b': 445.33,
    'c': 'Mike Smith'
}
logging.basicConfig(level=logging.INFO)

my_dict_obj = TplDictC(my_init_dict)

my_dict_obj.update(user_dict)

for (key, value) in my_dict_obj.items():
    print(key,value)

xx = my_init_dict
xx.update(user_dict, m)