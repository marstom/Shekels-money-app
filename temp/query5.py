from temp.t1 import session, Address, User

q = session.query(User.name, User.id)

for x in q:
    print(x)
    # print(x.name, x.fullname)