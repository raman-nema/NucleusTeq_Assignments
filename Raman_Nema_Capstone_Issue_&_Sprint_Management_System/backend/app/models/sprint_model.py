from datetime import datetime, time
from bson import ObjectId


class SprintModel:
    """Sprint document model."""

    @staticmethod
    def build(
        project_id: str,
        name: str,
        goal: str,
        start_date,
        end_date,
        created_by: str,
    ):
        """Create a sprint document."""

        # Capture current UTC timestamp.
        current_time = datetime.utcnow()

        return {
            # Convert project ID to MongoDB ObjectId.
            "project_id": ObjectId(project_id),
            "name": name,
            "goal": goal,
            # Store start date at the beginning of the day.
            "start_date": datetime.combine(
                start_date,
                time.min,
            ),
            # Store end date at the beginning of the day.
            "end_date": datetime.combine(
                end_date,
                time.min,
            ),
            # Default sprint status.
            "status": "PLANNED",
            "created_by": created_by,
            # Audit fields.
            "created_at": current_time,
            "updated_at": current_time,
        }
