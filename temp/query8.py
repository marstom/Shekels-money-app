from sqlalchemy.orm import eagerload

from temp.t1 import session, Address, User

q = session.query(User).join(
    Address
).filter(Address.value.like('%jakis%')).options(
    eagerload('addresses')
)


for x in q:
    print(x)
    for y in x.addresses:
        print(y.value)
    # print(x.name, x.fullname)
