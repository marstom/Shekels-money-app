from temp.t1 import session, Address

a = Address(value='address 2', user_id=1)
session.add(a)
session.commit()