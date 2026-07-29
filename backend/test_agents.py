import sys
import os

# Add backend directory to python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.agents.graph import orchestrator

def test_all_agents():
    print("=" * 60)
    print("🧪 TESTING ALL CONTEXTFORGE AI MULTI-AGENT PIPELINE NODES")
    print("=" * 60)

    prompt = "Add EMI payment option to orders table with DataHub schema verification"
    project_id = "proj-test-123"

    print(f"\n1. 📥 Input Prompt: '{prompt}'")
    print(f"2. 🆔 Project ID: '{project_id}'")

    print("\n------------------------------------------------------------")
    print("🤖 Executing MultiAgentOrchestrator...")
    print("------------------------------------------------------------")

    try:
        final_state = orchestrator.run_pipeline(prompt, project_id)

        print("\n✅ AGENT 1: PLANNER AGENT")
        print(f"   Task Plan: {final_state.task_plan}")

        print("\n✅ AGENT 2: CONTEXT AGENT (DataHub MCP)")
        print(f"   DataHub Context: {final_state.datahub_context}")

        print("\n✅ AGENT 3: IMPACT ANALYSIS AGENT")
        print(f"   Impact Assessment: {final_state.impact_assessment}")

        final_state = orchestrator.generate_code_after_approval(final_state)

        print("\n✅ AGENT 4: CODE GENERATOR AGENT")
        print(f"   Generated Code Snippet Preview:")
        print(f"   {final_state.generated_code[:200]}...")

        print("\n✅ PIPELINE STATUS:", final_state.current_node.upper())
        print("\n🎉 SUCCESS! All 4 AI Agents executed cleanly with 0 errors!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR during agent execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_all_agents()
