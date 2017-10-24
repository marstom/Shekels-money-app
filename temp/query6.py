from temp.t1 import session, Address, User

q = session.query(User, Address).join(
    Address,
    User.id == Address.user_id
)

for x in q:
    print(x)
    print(x[0], x[1])
    # print(x.name, x.fullname)
