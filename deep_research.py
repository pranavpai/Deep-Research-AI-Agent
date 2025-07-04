import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

# Create a single instance
research_manager = ResearchManager()

async def get_clarifications(query: str):
    """Generate clarification questions for the query with progress feedback"""
    if not query.strip():
        yield "Please enter a research query first.", gr.update(visible=False), gr.update(visible=False), gr.update(value="")
        return
    
    # Show progress
    yield "🔍 Generating clarification questions...", gr.update(visible=False), gr.update(visible=False), gr.update(value="")
    
    try:
        clarifications = await research_manager.get_clarification_questions(query)
        
        # Format questions for display
        questions_text = "**Clarifying Questions:**\n\n"
        for i, q in enumerate(clarifications.questions, 1):
            questions_text += f"**{i}. {q.question}**\n"
            questions_text += f"*({q.category} - {q.purpose})*\n\n"
        
        questions_text += "\n*Please answer the questions above in the box below (one answer per line), then click 'Start Research'*"
        
        # Store questions as JSON string for later use
        import json
        questions_data = json.dumps([{
            "question": q.question,
            "purpose": q.purpose,
            "category": q.category
        } for q in clarifications.questions])
        
        yield (
            questions_text,
            gr.update(visible=True),    # Show answers textbox
            gr.update(visible=True),    # Show start research button
            gr.update(value=questions_data)  # Store questions data
        )
    except Exception as e:
        yield f"Error generating clarifications: {str(e)}", gr.update(visible=False), gr.update(visible=False), gr.update(value="")

async def start_research(query: str, clarification_answers: str, questions_data: str):
    """Start research with the query, clarification questions, and answers"""
    if not query.strip():
        yield "Please enter a research query first."
        return
    
    try:
        # Parse questions data
        import json
        questions = []
        if questions_data.strip():
            try:
                questions = json.loads(questions_data)
            except:
                questions = []
        
        async for chunk in research_manager.run_research_workflow(query, clarification_answers, questions):
            yield chunk
    except Exception as e:
        yield f"Error during research: {str(e)}"

# Simple UI with minimal clarification handling
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    
    # Main query input
    query_textbox = gr.Textbox(
        label="What topic would you like to research?",
        placeholder="Enter your research query here...",
        lines=2
    )
    
    # Get clarifications button
    get_questions_btn = gr.Button("Get Clarification Questions", variant="primary")
    
    # Questions display
    questions_display = gr.Markdown(value="", visible=True)
    
    # Clarification answers (initially hidden)
    clarification_answers = gr.Textbox(
        label="Your answers to the clarification questions",
        placeholder="Answer each question on a separate line...",
        lines=3,
        visible=False
    )
    
    # Start research button (initially hidden)
    start_research_btn = gr.Button("Start Research", variant="primary", visible=False)
    
    # Hidden storage for questions data
    questions_storage = gr.Textbox(visible=False, value="")
    
    # Results
    report = gr.Markdown(label="Report")
    
    # Event handlers
    get_questions_btn.click(
        fn=get_clarifications,
        inputs=[query_textbox],
        outputs=[questions_display, clarification_answers, start_research_btn, questions_storage]
    )
    
    start_research_btn.click(
        fn=start_research,
        inputs=[query_textbox, clarification_answers, questions_storage],
        outputs=[report]
    )
    
    # Allow Enter in query to get questions
    query_textbox.submit(
        fn=get_clarifications,
        inputs=[query_textbox],
        outputs=[questions_display, clarification_answers, start_research_btn, questions_storage]
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True)