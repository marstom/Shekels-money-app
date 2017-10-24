from temp.t1 import session, User

q = session.query(User).filter(User.id == 2)

for x in q:
    print("USER!!")
    print(x.id)
    print(x.name)
    print(x.fullname)
