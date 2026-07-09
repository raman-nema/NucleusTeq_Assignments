from datetime import datetime, time
from bson import ObjectId


class SprintModel:
    @staticmethod
    def build(
        project_id: str,
        name: str,
        goal: str,
        start_date,
        end_date,
        status: str,
        created_by: str,
    ):
        current_time = datetime.utcnow()

        return {
            "project_id": ObjectId(project_id),
            "name": name,
            "goal": goal,
            "start_date": datetime.combine(
                start_date,
                time.min,
            ),
            "end_date": datetime.combine(
                end_date,
                time.min,
            ),
            "status": status,
            "created_by": created_by,
            "created_at": current_time,
            "updated_at": current_time,
        }
