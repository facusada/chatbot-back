from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import get_settings

ENGINE = create_engine(get_settings().database_url, future=True, echo=False)
SessionLocal = sessionmaker(bind=ENGINE, expire_on_commit=False, class_=Session)
Base = declarative_base()


@contextmanager
def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
