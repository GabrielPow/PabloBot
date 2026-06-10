from agents.agents import ingestion_agent

# Simulation A: Hits the explicit Rules-based engine
user_query_A = "Can you check what our runway looks like right now?"
decision_A = ingestion_agent(user_query_A)
print(f"Track: {decision_A.track} | Intent: {decision_A.analytical_intent}")
# Output: Track: Financial | Intent: calculate_burn_rate

# Simulation B: Complex sentence triggers Gemini's reasoning
user_query_B = "Our onboarding flows are leaking users between signing up and executing their first transaction, investigate Q1 trends."
decision_B = ingestion_agent(user_query_B)

print(decision_B.model_dump_json(indent=2))