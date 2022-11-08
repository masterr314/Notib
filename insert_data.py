import datetime

from sqlalchemy import *
from models import *

session = Session()

user_1 = User(user_id=1, username="bebebeu", first_name="Bohdan", last_name="anonim",
              birthData=datetime.datetime.now(), email="1234@k.com",
              password="12345", phone="123456")
user_2 = User(user_id=2, username="ia", first_name="donkey", last_name="empty",
              birthData=datetime.datetime.now(), email="ia@gmao.com",
              password="6789", phone="6789")

location_1 = Location(location_id=1, street="Street: 12", city="Lviv", region="West",
                      country="Ukraine", zip='12345')
location_2 = Location(location_id=2, street="Street: 13", city="Uzhorod", region="West",
                      country="Ukraine", zip='56789')

notice_1 = Notice(notice_id=1, title="Iphone Pro Max Ultra Geek", text="jsjflasjdlf",
                  createdAt='2022-10-11',
                  endAt='2022-10-11', type='local',
                  fk_user_id=1, fk_location_id=1)
notice_2 = Notice(notice_id=2, title="Iphone Mega Lux", text="qwerty",
                  createdAt='2022/10/11',
                  endAt='2022/10/11', type='local',
                  fk_user_id=2, fk_location_id=2)
#
group = Group(group_id=1, name="Phone", description="Everything about phone")
#
tag_1 = Tag(tag_id=1, name="lowest_price", color="Yellow", isActive=True)
tag_2 = Tag(tag_id=2, name="sale", color="Red", isActive=True)


tag_notice_1 = Tag_has_Notice(fk_tag_id=1, fk_notice_id=1)
tag_notice_2 = Tag_has_Notice(fk_tag_id=2, fk_notice_id=1)


session.add(user_1)
session.add(user_2)

session.add(location_1)
session.add(location_2)

session.commit()

session.add(notice_1)
session.add(notice_2)

session.add(tag_1)
session.add(tag_2)

session.add(group)

session.add(tag_notice_1)
session.add(tag_notice_2)

session.commit()
