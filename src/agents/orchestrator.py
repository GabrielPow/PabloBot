# agents/orchestrator.py
from agents.ingestion import IngestionAgent
from agents.execution import ExecutionAgent
from agents.synthesis import SynthesisAgent

class Orchestrator:
    def __init__(self):
        self.ingestion_agent = IngestionAgent()
        self.execution_agent = ExecutionAgent()
        self.synthesis_agent = SynthesisAgent()

    async def run_pipeline(self, user_task: str, context_data: str) -> str:
        print("\n--- [Orchestrator] Starting Pipeline ---")
        
        # Step 1: Figure out what the user wants
        intent = await self.ingestion_agent.determine_intent(user_task, context_data)
        
        # Step 2: Execute the specific function matching that intent
        execution_results = await self.execution_agent.execute_intent(intent)
        
        # Step 3: Synthesize results into insights
        final_insights = await self.synthesis_agent.generate_insights(user_task, execution_results)
        
        print("--- [Orchestrator] Pipeline Complete ---")
        return final_insights