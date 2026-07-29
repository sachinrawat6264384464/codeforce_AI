from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    user_prompt: str
    project_id: str
    task_plan: Optional[Dict[str, Any]] = None
    datahub_context: Optional[Dict[str, Any]] = None
    impact_assessment: Optional[Dict[str, Any]] = None
    generated_code: Optional[str] = None
    review_status: Optional[str] = None
    current_node: str = Field(default="planner")
