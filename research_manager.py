from agents import Runner, Agent, function_tool, trace, gen_trace_id
from clarifier_agent import clarifier_agent, ClarificationQuestions
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio
from typing import Dict, Any

# Define function tools for each agent
@function_tool
async def get_clarification_questions(query: str) -> Dict[str, Any]:
    """Generate clarification questions for a research query"""
    result = await Runner.run(clarifier_agent, f"Research Query: {query}")
    clarifications = result.final_output_as(ClarificationQuestions)
    return {
        "questions": [{"question": q.question, "purpose": q.purpose, "category": q.category} 
                     for q in clarifications.questions],
        "reasoning": clarifications.reasoning
    }

@function_tool
async def plan_research_searches(research_context: str) -> Dict[str, Any]:
    """Plan web searches based on research context including clarifications"""
    result = await Runner.run(planner_agent, research_context)
    search_plan = result.final_output_as(WebSearchPlan)
    return {
        "searches": [{"reason": s.reason, "query": s.query, "priority": s.priority} 
                    for s in search_plan.searches],
        "strategy": search_plan.search_strategy
    }

@function_tool
async def perform_web_search(search_query: str, search_reason: str) -> str:
    """Perform a single web search"""
    input_text = f"Search term: {search_query}\nReason for searching: {search_reason}"
    try:
        result = await Runner.run(search_agent, input_text)
        return str(result.final_output)
    except Exception as e:
        return f"Search failed: {e}"

@function_tool
async def write_research_report(research_context: str, search_results: str) -> Dict[str, Any]:
    """Write a comprehensive research report"""
    input_text = f"{research_context}\n\nSummarized search results: {search_results}"
    result = await Runner.run(writer_agent, input_text)
    report = result.final_output_as(ReportData)
    return {
        "short_summary": report.short_summary,
        "markdown_report": report.markdown_report,
        "follow_up_questions": report.follow_up_questions
    }

@function_tool
async def send_research_email(report_content: str) -> Dict[str, str]:
    """Send research report via email"""
    result = await Runner.run(email_agent, report_content)
    return {"status": "sent", "message": "Research report sent successfully"}

# Manager Agent with handoffs
MANAGER_INSTRUCTIONS = """You are a research manager that coordinates a team of specialized agents to conduct comprehensive research.

Your workflow:
1. For clarification queries: Use get_clarification_questions to generate intelligent questions
2. For research requests: 
   - Use plan_research_searches to create a search strategy
   - Use perform_web_search for each planned search
   - Use write_research_report to synthesize findings
   - Use send_research_email to deliver the report

Always follow this sequence and use the appropriate tools for each step. Provide clear status updates throughout the process."""

manager_agent = Agent(
    name="ResearchManagerAgent",
    instructions=MANAGER_INSTRUCTIONS,
    tools=[get_clarification_questions, plan_research_searches, perform_web_search, write_research_report, send_research_email],
    model="gpt-4o-mini"
)

class ResearchManager:
    """Wrapper class to maintain compatibility while using Agent underneath"""
    
    async def get_clarification_questions(self, query: str) -> ClarificationQuestions:
        """Get clarification questions for a research query"""
        print("Generating clarification questions...")
        result = await Runner.run(
            manager_agent,
            f"Generate clarification questions for this research query: {query}"
        )
        
        # Parse the agent response to extract clarifications
        try:
            clarifications_data = result.final_output
            # Convert back to ClarificationQuestions format
            questions = []
            if isinstance(clarifications_data, dict) and "questions" in clarifications_data:
                from clarifier_agent import ClarifyingQuestion
                for q_data in clarifications_data["questions"]:
                    questions.append(ClarifyingQuestion(
                        question=q_data["question"],
                        purpose=q_data["purpose"],
                        category=q_data["category"]
                    ))
            
            return ClarificationQuestions(
                questions=questions,
                reasoning=clarifications_data.get("reasoning", "Generated clarification questions")
            )
        except:
            # Fallback: call clarifier directly
            result = await Runner.run(clarifier_agent, f"Research Query: {query}")
            return result.final_output_as(ClarificationQuestions)
    
    async def run_research_workflow(self, query: str, clarifications: str = "", questions: list = None):
        """Run the complete research workflow with optional clarifications and questions"""
        trace_id = gen_trace_id()
        with trace("Enhanced Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            
            # Create research context with questions and answers
            research_context = self.create_research_context(query, clarifications, questions)
            yield "Research context prepared..."
            
            # Use manager agent to coordinate the research
            instruction = f"""Conduct comprehensive research using this context:

{research_context}

Follow the complete research workflow:
1. Plan searches based on the context and clarifications
2. Execute all planned searches
3. Write a comprehensive report
4. Send the report via email

Provide status updates for each step."""
            
            # Always use fallback workflow for reliability and full report display
            async for chunk in self._fallback_workflow(research_context):
                yield chunk

    async def _fallback_workflow(self, research_context: str):
        """Fallback workflow if manager agent fails"""
        try:
            # Plan searches
            result = await Runner.run(planner_agent, research_context)
            search_plan = result.final_output_as(WebSearchPlan)
            yield "Searches planned, starting to search..."
            
            # Perform searches
            search_results = []
            for i, search_item in enumerate(search_plan.searches):
                try:
                    result = await Runner.run(
                        search_agent,
                        f"Search term: {search_item.query}\nReason for searching: {search_item.reason}"
                    )
                    search_results.append(str(result.final_output))
                    yield f"Search {i+1}/{len(search_plan.searches)} completed"
                except:
                    continue
            
            yield "Searches complete, writing report..."
            
            # Write report
            result = await Runner.run(
                writer_agent,
                f"{research_context}\n\nSearch results: {search_results}"
            )
            report = result.final_output_as(ReportData)
            
            yield "Report written, sending email..."
            
            # Send email
            await Runner.run(email_agent, report.markdown_report)
            yield "Email sent, research complete"
            yield report.markdown_report
            
        except Exception as e:
            yield f"Fallback workflow failed: {e}"

    async def run(self, query: str):
        """Simple run method for backward compatibility"""
        async for chunk in self.run_research_workflow(query, "", None):
            yield chunk

    def create_research_context(self, query: str, clarifications: str, questions: list = None) -> str:
        """Create research context from query, clarifications, and questions"""
        context_parts = [
            "=== RESEARCH CONTEXT ===",
            f"Original Query: {query}"
        ]
        
        if clarifications.strip() and questions:
            context_parts.append(f"\n=== CLARIFYING QUESTIONS & ANSWERS ===")
            context_parts.append("The user was asked clarifying questions and provided these specific responses:")
            
            # Parse clarifications (assume one per line)
            clarification_lines = [line.strip() for line in clarifications.strip().split('\n') if line.strip()]
            
            # Match questions with answers
            for i, (question_data, answer) in enumerate(zip(questions, clarification_lines), 1):
                if i <= len(clarification_lines):
                    context_parts.append(f"\n**Question {i} ({question_data.get('category', 'general')}):** {question_data.get('question', 'N/A')}")
                    context_parts.append(f"**User's Answer:** {answer}")
                    context_parts.append(f"**Purpose:** {question_data.get('purpose', 'N/A')}")
                else:
                    # Question without answer
                    context_parts.append(f"\n**Question {i} ({question_data.get('category', 'general')}):** {question_data.get('question', 'N/A')}")
                    context_parts.append(f"**User's Answer:** [No answer provided]")
                    context_parts.append(f"**Purpose:** {question_data.get('purpose', 'N/A')}")
            
            context_parts.append(f"\n=== SEARCH PLANNING REQUIREMENTS ===")
            context_parts.append("- Each search must directly address the user's clarified needs above")
            context_parts.append("- Prioritize searches based on the question categories and user responses")
            context_parts.append("- Tailor search depth and perspective to the clarified audience and purpose")
            context_parts.append("- Consider the clarified constraints (timeline, geography, scope, etc.)")
            context_parts.append("- Use the question purposes to guide search strategy")
            
        elif clarifications.strip():
            # Fallback for when we have answers but no questions structure
            context_parts.append(f"\n=== USER CLARIFICATIONS ===")
            context_parts.append("The user provided these specific clarifications to focus the research:")
            
            clarification_lines = [line.strip() for line in clarifications.strip().split('\n') if line.strip()]
            for i, clarification in enumerate(clarification_lines, 1):
                context_parts.append(f"{i}. {clarification}")
            
            context_parts.append(f"\n=== SEARCH PLANNING REQUIREMENTS ===")
            context_parts.append("- Each search must directly address at least one of the user clarifications above")
            context_parts.append("- Prioritize searches that serve the user's specific focus areas")
            
        else:
            context_parts.append(f"\n=== SEARCH PLANNING REQUIREMENTS ===")
            context_parts.append("- No specific clarifications provided")
            context_parts.append("- Plan comprehensive searches covering multiple angles of the topic")
        
        return "\n".join(context_parts)