#!/usr/bin/env python3
"""
Enhanced Deep Research Agent - Main Entry Point

This is the main entry point for the Enhanced Deep Research Agent system.
It provides a ChatGPT-like deep research experience with clarification questions,
intelligent search planning, and comprehensive report generation.

Features:
- Intelligent clarification questions based on user queries
- Multi-agent orchestration with handoffs
- Contextual search planning and execution
- Comprehensive report generation
- Email delivery of results
- Modern Gradio interface

Usage:
    python main.py

Environment Variables Required:
- OPENAI_API_KEY: Your OpenAI API key
- SENDGRID_API_KEY: SendGrid API key for email delivery
- HF_TOKEN: Hugging Face token (optional)
- PUSHOVER_USER/TOKEN: Pushover notifications (optional)
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
import gradio as gr

# Import our application
from deep_research import ui as research_interface

def check_environment():
    """Check if all required environment variables are set."""
    
    required_vars = ["OPENAI_API_KEY", "SENDGRID_API_KEY", "FROM_EMAIL", "TO_EMAIL"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        return False
    
    print("✅ Environment variables check passed")
    return True

def print_startup_info():
    """Print startup information."""
    
    print("🔬 Enhanced Deep Research Agent")
    print("=" * 50)
    print("Features:")
    print("  • Intelligent clarification questions")
    print("  • Multi-agent research orchestration")
    print("  • Comprehensive report generation")
    print("  • Email delivery")
    print("  • Modern web interface")
    print("")
    print("Starting application...")
    print("")

def main():
    """Main entry point."""
    
    # Load environment variables
    load_dotenv(override=True)
    
    # Print startup info
    print_startup_info()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    try:
        # Use the interface from deep_research
        app = research_interface
        
        print("🚀 Launching Enhanced Deep Research Agent...")
        print("📱 Interface will open in your browser automatically")
        print("🔗 Access URL: http://localhost:7860")
        print("")
        print("💡 Tips:")
        print("  • Try the example queries to get started")
        print("  • Use clarification questions for better results")
        print("  • Check your email for detailed reports")
        print("")
        print("Press Ctrl+C to stop the application")
        print("-" * 50)
        
        # Launch the application
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            inbrowser=True,
            show_error=True,
            quiet=False
        )
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Enhanced Deep Research Agent...")
        print("Thank you for using the system!")
        
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        print("Please check the logs and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()