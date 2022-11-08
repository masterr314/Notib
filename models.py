from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import MetaData
import sqlalchemy.orm

Base = declarative_base()
sql_engine = create_engine('mysql://root:lehyfz_[fnf@localhost:3306/laba_6_pp',
                           echo=False)
Session = sessionmaker(bind=sql_engine)
session = Session()
metadata = Base.metadata


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True,
                     nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    email = Column(String(45), unique=True, nullable=False)
    password = Column(String(45), nullable=False)
    is_superuser = Column(Enum("true", "false"), default="false")


class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True, autoincrement=True,
                         nullable=False)
    category_name = Column(String(45), unique=True)


class SubCategory(Base):
    __tablename__ = "sub_category"
    sub_category_id = Column(Integer, primary_key=True, autoincrement=True,
                             nullable=False)
    sub_category_name = Column(String(45), nullable=False, unique=True)
    fk_category_id = Column(Integer, ForeignKey("category.category_id"),
                            primary_key=True, nullable=False)
    category = sqlalchemy.orm.relationship(Category)


class Producer(Base):
    __tablename__ = "producer"
    producer_id = Column(Integer, primary_key=True, autoincrement=True,
                         nullable=False)
    producing_company = Column(String(45), nullable=False)
    producing_country = Column(String(45), nullable=False)


class Dosed(Base):
    __tablename__ = "dosed"
    dosed_id = Column(Integer, primary_key=True, autoincrement=True,
                      nullable=False)
    dosed_name = Column(String(45), nullable=False)
    dosed_description = Column(String(45), nullable=False)
    dosed_form = Column(
        Enum("capsules", "pills", "dragee", "granules", "powders", "solutions",
             "infusions",
             "tinctures", "liquid extracts", "emulsions", "mixtures"),
        nullable=False)
    physical_form = Column(Enum("solid", "liquid"), nullable=False)
    the_number_of_blisters = Column(SmallInteger, default=null)
    quantity_in_package = Column(SmallInteger, default=null)
    net_weight = Column(Float, nullable=False)
    unit_of_measurement = Column(Enum("ml", "l", "mg", "gr"), nullable=False)
    for_a_prescription = Column(Enum("true", "false"), nullable=False)
    dosed_price = Column(Float, nullable=False)
    fk_producer_id = Column(Integer, ForeignKey("producer.producer_id"),
                            primary_key=True, nullable=False)
    fk_sub_category_id = Column(Integer,
                                ForeignKey("sub_category.sub_category_id"),
                                primary_key=True, nullable=False)
    sub_category = sqlalchemy.orm.relationship(SubCategory)
    producer = sqlalchemy.orm.relationship(Producer)


class Undosed(Base):
    __tablename__ = 'undosed'
    undosed_id = Column(Integer, primary_key=True, autoincrement=True,
                        nullable=False)
    undosed_name = Column(String(45), nullable=False)
    undosed_description = Column(String(45), nullable=False)
    undosed_form = Column(
        Enum("ointments", "linimets", "pastes", "suppositories", "plasters"),
        nullable=False)
    physical_form = Column(Enum("gaseous", "semi-solid"), nullable=False)
    net_weight = Column(Float, nullable=False)
    unit_of_measurement = Column(Enum("ml", "l", "mg", "gr"), nullable=False)
    for_a_prescription = Column(Enum("true", "false"), nullable=False)
    dosed_price = Column(Float, nullable=False)
    fk_producer_id = Column(Integer, ForeignKey("producer.producer_id"),
                            primary_key=True, nullable=False)
    fk_sub_category_id = Column(Integer,
                                ForeignKey("sub_category.sub_category_id"),
                                primary_key=True, nullable=False)
    sub_category = sqlalchemy.orm.relationship(SubCategory)
    producer = sqlalchemy.orm.relationship(Producer)


class MedicineHasStorage(Base):
    __tablename__ = "medicine_has_storage"
    storage_id = Column(Integer, primary_key=True, autoincrement=True,
                        nullable=False)
    quantity = Column(Integer, nullable=False)
    valid_until = Column(Date, nullable=False)
    fk_undosed_id = Column(Integer, ForeignKey("undosed.undosed_id"),
                           primary_key=True, nullable=False)
    fk_dosed_id = Column(Integer, ForeignKey("dosed.dosed_id"),
                         primary_key=True, nullable=False)
    undosed = sqlalchemy.orm.relationship(Undosed)
    dosed = sqlalchemy.orm.relationship(Dosed)


class Cart(Base):
    __tablename__ = "cart"
    cart_id = Column(Integer, primary_key=True, autoincrement=True,
                     nullable=False)
    fk_dosed_id = Column(Integer, ForeignKey("dosed.dosed_id"), nullable=False)
    fk_undosed_id = Column(Integer, ForeignKey("undosed.undosed_id"),
                           nullable=False)
    dosed = sqlalchemy.orm.relationship(Dosed)
    undosed = sqlalchemy.orm.relationship(Undosed)


class Order(Base):
    __tablename__ = "order"
    order_id = Column(Integer, primary_key=True, autoincrement=True,
                      nullable=False)
    fk_user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True,
                        nullable=False)
    fk_cart_id = Column(Integer, ForeignKey("cart.cart_id"), nullable=False)
    date_of_purchase = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    user = sqlalchemy.orm.relationship(User)
    cart = sqlalchemy.orm.relationship(Cart)
