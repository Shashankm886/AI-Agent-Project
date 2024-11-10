import streamlit as st
from ai_agent_backend import process_user_input
from conversation_manager import ConversationManager

# Initialize conversation manager
if 'conversation_manager' not in st.session_state:
    st.session_state.conversation_manager = ConversationManager()
    st.session_state['feature'] = None  # Track the selected feature
    st.session_state['additional_input'] = ""  # Additional input based on feature

st.title("AI Agent")

st.write("""
This AI Agent can fetch cryptocurrency prices, handle language translation requests, and answer general cryptocurrency-related queries, while maintaining English as its primary communication language.
""")
st.markdown("---")

# Feature selection and input based on selected feature
feature_options = ["Show Price of Cryptocurrency", "Change Language of Prompt", "General Query Regarding Cryptocurrency Prices"]
selected_feature = st.selectbox("Select a feature to proceed:", feature_options)

st.session_state['feature'] = selected_feature

# Prompt for additional input based on selected feature
if selected_feature == "Show Price of Cryptocurrency":
    st.session_state['additional_input'] = st.text_input("Enter the name of the cryptocurrency:")
elif selected_feature == "Change Language of Prompt":
    st.session_state['additional_input'] = st.text_input("Enter the new language for the prompt:")
elif selected_feature == "General Query Regarding Cryptocurrency Prices":
    st.session_state['additional_input'] = st.text_input("Enter your query about cryptocurrency:")

st.markdown("---")

# displaying conversation in a reverse order
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# reversed so that the newest messages are at the bottom
for message in reversed(st.session_state['messages']):
    if message['role'] == 'user':
        st.markdown(f"**You:** {message['content']}")
    elif message['role'] == 'assistant':
        st.markdown(f"**Assistant:** {message['content']}")

# Message submission form at the bottom
with st.form(key='message_form', clear_on_submit=True):
    submitted = st.form_submit_button("Send")
    if submitted and st.session_state['additional_input'].strip() != "":
        user_input = st.session_state['additional_input']
        
        # Modify the prompt based on the selected feature
        if st.session_state['feature'] == "Show Price of Cryptocurrency":
            modified_input = f"show price of {user_input}"
        elif st.session_state['feature'] == "Change Language of Prompt":
            modified_input = f"change language to {user_input}"
        else:
            modified_input = user_input  # For general queries, use input as-is
        
        # Process the modified input
        try:
            response = process_user_input(modified_input, st.session_state['conversation_manager'])
            # Append messages with newest at the bottom
            st.session_state['messages'].append({'role': 'user', 'content': user_input})
            st.session_state['messages'].append({'role': 'assistant', 'content': response})
            # Rerun to display the updated conversation
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")
