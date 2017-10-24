from temp.t1 import session, User

u1 = User(name='First', fullname='F1')
session.add(u1)
session.commit()
