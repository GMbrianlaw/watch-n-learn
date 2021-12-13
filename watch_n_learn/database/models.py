from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from watch_n_learn.database.main import DATABASE_ENGINE

Base = declarative_base(DATABASE_ENGINE)

class User(Base):

    __tablename__ = "User"

    id_ = Column("UserID", Integer(), primary_key=True)

    name = Column("Name", String(32), nullable=False)

    username = Column("Username", String(16), nullable=False, unique=True)

    hashed_password = Column("HashedPassword", String(64), nullable=False)

    posts = relationship(
        "Post", back_populates="user", order_by="Post.time.desc()"
    )

class Post(Base):

    __tablename__ = "Post"

    id_ = Column("PostID", Integer(), primary_key=True)

    user_id = Column("UserID", Integer(), ForeignKey(User.id_), nullable=False)

    title = Column("Title", String(256), nullable=False)

    content = Column("Content", String(4096), nullable=False)

    time = Column("Time", DateTime(), nullable=False, server_default=now())

    user = relationship(User, back_populates="posts")
