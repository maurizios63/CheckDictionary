import logging
from TplPkg import TplList
logging.basicConfig(level=logging.INFO)

a = [1.0,2]
ref_list = [2, 1.0, {}]
x = TplList(a, ref_list=ref_list)
logging.info(x)
logging.info("Using append")
x.append(3)
x.append(3.4)
x.append('xx')
x.append({'xx': 1, 'yy': 2})
logging.info(x)