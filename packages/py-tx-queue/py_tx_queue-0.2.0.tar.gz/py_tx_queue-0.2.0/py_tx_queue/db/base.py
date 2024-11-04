import os
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB as JSON, BIGINT, ENUM as SQLEnum, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum, unique


Base = declarative_base()


def new_async_session_local() -> async_sessionmaker[AsyncSession]:
    DATABASE_URL = os.environ["PY_TX_QUEUE_DATABASE_URL"]

    engine = create_async_engine(
        DATABASE_URL
    )

    AsyncSessionLocal = async_sessionmaker(
        expire_on_commit=False,
        # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#flushing
        autoflush=False,
        bind=engine,
    )

    return AsyncSessionLocal


@unique
class JobStatus(Enum):
    INSERTED = "inserted"
    EXECUTING = "executing"
    CANCELLED = "cancelled"
    SCHEDULED = "scheduled"
    RETRYABLE = "retryable"
    DISCARDED = "discarded"
    COMPLETED = "completed"


class PyTxQueueJob(Base):
    __tablename__ = "py_tx_queue__jobs"

    # Internal ID
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)

    # External ID, if provided, the user can use it to identify the job
    # as it's an indexed column
    external_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)

    # Base information of the job
    queue: Mapped[str] = mapped_column(String, nullable=False, index=True)
    worker: Mapped[str] = mapped_column(String, nullable=False, index=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Status of the job
    status: Mapped[JobStatus] = mapped_column(SQLEnum(JobStatus), default=JobStatus.INSERTED, nullable=False, index=True)

    # When the job was inserted into the queue
    inserted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # When the job was scheduled to run
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # When the job was last attempted
    attempted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    discarded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # When the job was completed, it may have been successful or not, check the status
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Last execution time
    elapsed_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    errors: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False)

    priority: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=[])
    meta: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
