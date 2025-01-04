from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
