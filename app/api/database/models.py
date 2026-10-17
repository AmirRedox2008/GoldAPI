from api.database.database import Base,engine
from sqlalchemy import String,Column,Float,Integer ,DateTime



class save_prices(Base):

    __tablename__ = "prices"

    id = Column (Integer,primary_key=True, index=True)
    name = Column(String)
    price = Column(String)
    change = Column(String)
    low = Column(String)
    high = Column(String)
    Updatetime = Column(DateTime)



Base.metadata.create_all(engine)