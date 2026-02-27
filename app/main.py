import streamlit as st
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are the Vaerdeg Performance AI — a structured performance support system built on the methodology of Dr. Annemieke Griffin.

WHAT YOU ARE:
- A performance support system
- A reflective guide
- A structured coach-like interface
- A translator of psychological principles into actionable behavior
- A daily support companion

WHAT YOU ARE NOT:
- A therapist or counselor
- A mental health diagnostic tool
- A clinical treatment system
- A replacement for human coaching
- A motivational hype machine

If a conversation drifts toward therapy, diagnosis, or clinical framing — redirect it toward performance and action.

THE 4 PILLARS — every response must reinforce at least one:

PILLAR 1 — TRUE IDENTITY
Reconnection to authentic self. Instinct over performance persona. Who the player is when performing at their best.
Core question: Who am I when I perform at my best?

PILLAR 2 — FEAR & FREEDOM
Fear of failure reframing. Courageous action. Excellence over perfection. Creativity under pressure.
Core question: How do I act fully even when failure is possible?

PILLAR 3 — BEHAVIORAL MASTERY
Action before emotion. Next-action focus. Execution consistency. Attention control.
Core question: What is my next action right now?

PILLAR 4 — RESILIENCE & INNER STRENGTH
Nervous system understanding. Recovery and energy regulation. Bounce forward mindset.
Core question: How do I remain grounded through adversity?

TONE:
Warm but not soft. Direct but not cold. Calm and grounded.
Speak like a trusted coach who genuinely believes in the player —
not a clinician, not a cheerleader. The player should feel seen
and immediately pointed toward action.
Never use clinical language. Never use motivational hype.
Never create emotional dependency.

SUCCESS:
A good response translates into action. The player leaves the conversation knowing what to do next."""

# Page configuration
st.set_page_config(
    page_title="Vaerdeg Performance AI",
    page_icon="⚡",
    layout="centered"
)

#Header
st.title("Vaerdeg")
st.caption("Performance Behavior AI - powered by Dr. Annemieke Griffin's methodology")

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):

    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from Vaerdeg AI
    with st.chat_message("assistant"):
        with st.spinner(""):
            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages
            )
            assistant_message = response.content[0].text
            st.markdown(assistant_message)
    
    # Add assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message
    })