from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Company, Camera, Lense

engine = create_engine('sqlite:///camerastudio.db')
# bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
ADMIN = User(name="admin", email="shak5643@gmail.com")
session.add(ADMIN)
session.commit()

# Create dummy company
COMPANY_1 = Company(name="Fujifilm")
session.add(COMPANY_1)
session.commit()

COMPANY_2 = Company(name="Sony")
session.add(COMPANY_2)
session.commit()

COMPANY_3 = Company(name="Canon")
session.add(COMPANY_3)
session.commit()

# Create dummy camera
CAMERA_1 = Camera(name="X-T20",
                  description="mirrorless interchangeable-lens camera announced"
                  "by Fujifilm on January 19,2017.",
                  wiki_url="https://en.wikipedia.org/wiki/Fujifilm_X-T20",
                  company_id=1
                  )
session.add(CAMERA_1)
session.commit()

CAMERA_2 = Camera(name="X-T2",
                  description="DSLR-style weather-resistant mirrorless camera"
                  "announced by Fujifilm on July 7, 2016",
                  wiki_url="https://en.wikipedia.org/wiki/Fujifilm_X-T2",
                  company_id=1
                  )
session.add(CAMERA_2)
session.commit()

CAMERA_3 = Camera(name="A7",
                  description="full-frame mirrorless interchangeable-lens"
                  "camera announced by Sony 16 October 2013",
                  wiki_url="https://en.wikipedia.org/wiki/Sony_%CE%B17#ILCE-7R",
                  company_id=2
                  )
session.add(CAMERA_3)
session.commit()

CAMERA_4 = Camera(name="EOS-7D",
                  description="professional cropped sensor digital single-lens"
                  "reflex camera made by Canon announced on 1 September 2009",
                  wiki_url="https://en.wikipedia.org/wiki/Canon_EOS_7D",
                  company_id=3
                  )
session.add(CAMERA_4)
session.commit()


print("Dummy data inserted!!")
