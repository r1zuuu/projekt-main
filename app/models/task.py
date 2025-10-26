from datetime import datetime

from sqlalchemy import Enum 

from . import db

STATUS_ENUM = ("pending", "in-progress", "completed")
PRIORITY_ENUM = ("low", "medium", "high")


class Task(db.Model):

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(
        Enum(*STATUS_ENUM, name="status_enum"), nullable=False, default="pending"
    )
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(
        Enum(*PRIORITY_ENUM, name="priority_enum"), nullable=False, default="medium"
    )

    user = db.relationship("User", back_populates="tasks")

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
        }
