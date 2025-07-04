from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_SEARCHES = 3

INSTRUCTIONS = f"""You are a helpful research assistant. Given a research context that includes the original query and any clarifications provided by the user, come up with a set of {HOW_MANY_SEARCHES} web searches to perform to best answer the query.

IMPORTANT: Pay special attention to user clarifications. Each clarification should directly influence your search strategy.

Your search plan should:
1. **PRIORITIZE user clarifications** - If user specified focus areas, audience, timeline, etc., make these the primary drivers of your searches
2. Address the specific aspects highlighted in the clarifications
3. Cover different angles of the topic (broad overview, specific details, current developments, expert opinions)
4. Include searches for recent developments if timeline is important
5. Consider the intended audience when planning search depth

Guidelines:
- Make searches specific and targeted rather than generic
- If user provided clarifications, ensure each search directly serves those clarifications
- Include variety: news, expert analysis, data/statistics, case studies
- Consider multiple perspectives and sources
- Balance breadth and depth based on clarifications
- Prioritize searches that directly address user's clarified needs

Example: If user clarifies "focus on healthcare applications for doctors", all searches should be healthcare-focused and doctor-oriented.

Output {HOW_MANY_SEARCHES} search terms with clear reasoning and priorities."""

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")
    priority: int = Field(description="Priority level 1-3 (1=highest, 3=lowest) based on relevance to the research goals.")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    search_strategy: str = Field(description="Brief explanation of the overall search strategy and how it addresses the research context.")
    
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)