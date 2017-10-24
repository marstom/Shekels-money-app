from temp.t1 import session, Address, User

q = session.query(User)

for x in q:
    print(x)
    print(x.name, x.fullname)