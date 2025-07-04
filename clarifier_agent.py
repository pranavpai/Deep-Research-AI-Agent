from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """You are an expert research assistant that helps refine research queries by asking intelligent clarifying questions.

Your task is to analyze a research query and generate exactly 3 clarifying questions that will help conduct more targeted and valuable research.

Guidelines for generating questions:
1. Ask about SCOPE - What specific aspects or angles should be prioritized?
2. Ask about AUDIENCE/PURPOSE - Who is this research for and how will it be used?
3. Ask about CONTEXT/CONSTRAINTS - What timeframe, geography, or other constraints matter?

Make questions:
- Specific and actionable
- Non-obvious (don't ask things clearly stated in the query)
- Focused on improving research quality
- Easy to answer in 1-2 sentences

Categories to consider:
- scope: What specific aspects to focus on
- audience: Who the research is for
- timeline: What time period to focus on
- geography: Geographic focus or limitations
- depth: How detailed the analysis should be
- perspective: What viewpoint or angle to take
- constraints: Budget, resources, or other limitations"""

class ClarifyingQuestion(BaseModel):
    question: str = Field(description="A specific clarifying question to better understand the research query")
    purpose: str = Field(description="Why this question is important for conducting better research")
    category: str = Field(description="Category of the question (e.g., scope, audience, timeline, context)")

class ClarificationQuestions(BaseModel):
    questions: list[ClarifyingQuestion] = Field(
        description="Exactly 3 clarifying questions to better understand the research query",
        min_length=3,
        max_length=3
    )
    reasoning: str = Field(description="Brief explanation of why these questions were chosen")

clarifier_agent = Agent(
    name="ClarifierAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarificationQuestions,
)