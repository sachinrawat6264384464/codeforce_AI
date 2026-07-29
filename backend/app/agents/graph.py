from app.agents.state import AgentState
from app.agents.planner.planner_agent import PlannerAgent
from app.agents.context.context_agent import ContextAgent
from app.agents.impact.impact_agent import ImpactAgent
from app.agents.generator.backend_generator import BackendGeneratorAgent
from app.agents.generator.frontend_generator import FrontendGeneratorAgent

class MultiAgentOrchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.context_agent = ContextAgent()
        self.impact_agent = ImpactAgent()
        self.backend_generator = BackendGeneratorAgent()
        self.frontend_generator = FrontendGeneratorAgent()

    def run_pipeline(self, user_prompt: str, project_id: str) -> AgentState:
        state = AgentState(user_prompt=user_prompt, project_id=project_id)
        
        # 1. Planner Node
        state.task_plan = self.planner.decompose_task(user_prompt)
        state.current_node = "context"
        
        # 2. Context Node (Mocked DataHub)
        state.datahub_context = self.context_agent.fetch_datahub_context("orders")
        state.current_node = "impact"
        
        # 3. Impact Analysis Node
        state.impact_assessment = self.impact_agent.evaluate_impact(state.datahub_context)
        state.current_node = "approval_pending"
        
        return state

    def generate_code_after_approval(self, state: AgentState) -> AgentState:
        modules = state.task_plan.get("tasks", ["orders"])
        
        # 4. Backend Generator Node (writes real FastAPI files to disk)
        backend_result = self.backend_generator.generate_files(state.project_id, state.user_prompt, modules)
        
        # 5. Frontend Generator Node (writes real Next.js TSX files to disk)
        frontend_result = self.frontend_generator.generate_files(state.project_id, state.user_prompt, modules)
        
        state.generated_code = f"Generated {len(backend_result['generated_files'])} Backend & {len(frontend_result['generated_files'])} Frontend files."
        state.current_node = "completed"
        
        return state

orchestrator = MultiAgentOrchestrator()
