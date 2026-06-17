import asyncio
from agents.ai_model import call_gemini_structured, IngestionRoutingSchema


# -------- INGESTOR --------- #

INGESTOR_SYSTEM_PROMPT = """
You are the primary Ingestion and Routing Agent for an advanced Enterprise Performance Analytics Engine.
Your sole job is to analyze the user's objective and map it to exactly ONE of our five core analytics tracks:
1. Financial (revenue, budget, runway, burn rate)
2. Operational (throughput, bottlenecks, supply chain efficiency)
3. People (turnover, hiring velocity, eNPS, talent acquisition)
4. Product (feature adoption, DAU/MAU, user friction)
5. Growth (CAC, LTV, conversion funnels, cohort retention)

Be analytical and strictly extract any extra filters (like dates, quarters, or percentages) into the conditionals object.
"""

# In Progress, rigged not to work exactly. REGEX Needs to be implemented
def run_rules_based_router(user_input: str):
    """
    Fast, cost-effective string checking. 
    Returns (track, intent) if matched, otherwise None.
    """
    input_lower = user_input.lower()
    
    # Example Rule 1: Financial Track Quick-route
    if "burn rate" in input_lower or "runway" in input_lower:
        return "Financial", "calculate_burn_rate", {"detected_via": "regex"}
        
    # Example Rule 2: Growth Track Quick-route
    if "cac" in input_lower or "customer acquisition cost" in input_lower:
        return "Growth", "calculate_cac_ratio", {"detected_via": "regex"}
        
    return None


# Receives prompt, checkes with rules_based match, if not decides to run LLM as a backup.
def ingestion_agent(user_input: str) -> IngestionRoutingSchema:
    """
    Orchestrates the ingestion step using a hybrid approach.
    """
    # 1. Try rules first
    rule_match = run_rules_based_router(user_input)
    if rule_match:
        track, intent, conds = rule_match
        return IngestionRoutingSchema(
            reasoning_chain="Matched explicit keyword filter rules-based routing.",
            track=track,
            analytical_intent=intent,
            conditionals=conds
        )
        
    # 2. Fallback to Gemini Structured Processing
    prompt = f"Analyze the following user input and route it accordingly:\n\nUser Input: '{user_input}'"
    
    try:
        routing_decision = call_gemini_structured(prompt, INGESTOR_SYSTEM_PROMPT)
        return routing_decision
    except Exception as e:
        # Graceful fallback error handling for pipeline resilience
        return IngestionRoutingSchema(
            reasoning_chain=f"Routing failed due to exception: {str(e)}",
            track="Unknown",
            analytical_intent="error_fallback",
            conditionals={"error": True}
        )

# -------- ORCHESTRATOR --------- #

class Orchestrator:
    def __init__(self):
        #self.agent = Agent()
        self

    async def run_pipeline(
        self,
        objective: str,
        source_hint: str = "",
    ) -> str:
        print("\n--- Orchestrator: starting pipeline ---")

        # Step 1: Understand the Context
        routing_decsision = await self

        # Step 2: Route the Decision
        qualified_json = await self.qualifier.qualify(raw_data, criteria)

        # Step 3: Interpret Data
        final_csv = await self

        # Step 4: Aglomerate Data / Understand Insights
        insights_csv = await self

        print("\n--- Orchestrator: pipeline complete ---")
        return final_csv