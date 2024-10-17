import streamlit as st
import requests

def main():
    # Set page config
    st.set_page_config(page_title="Azure OpenAI Chat", page_icon="🤖")
    st.title("Azure OpenAI GPT-4o Chat Interface")

    # Set a background color for the whole app
    st.markdown("""
        <style>
        .reportview-container {
            background-color: #f0f0f5;  /* Light gray background color */
        }
        </style>
        """, unsafe_allow_html=True)

    # Azure OpenAI connection details
    azure_openai_key = "YOUR_AZURE_OPENAI_KEY"  # Replace with your actual key
    azure_openai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"  # Replace with your actual endpoint URL

    # Store chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history with improved layout
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f"<div style='text-align: right; border-radius: 10px; padding: 10px; margin: 5px; max-width: 80%; display: inline-block;'><strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; border-radius: 10px; padding: 10px; margin: 5px; max-width: 80%; display: inline-block;'><strong>AI:</strong> {msg['content']}</div>", unsafe_allow_html=True)

    # Create a container for user input and the send button
    col1, col2 = st.columns([1, 0.1])  # Create two columns for layout

    with col1:
        user_input = st.text_input("Your Message:", "", key="input", placeholder="Type your message here...", label_visibility="visible")  # Ensure the label is visible

    with col2:
        # Add margin top using st.markdown
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)  # Adjust the margin as needed
        # Send button as an icon
        if st.button("📝", key="send", help="Send message"):
            # Only proceed if there's user input
            if user_input:
                # Append user message to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})

                try:
                    headers = {
                        "Content-Type": "application/json",
                        "api-key": azure_openai_key
                    }
                    
                    data = {
                        "messages": [{"role": "user", "content": user_input}],
                        "max_tokens": 1000,  # Adjust the token limit as needed
                        "temperature": 0.7  # Control the randomness of the output
                    }
                    
                    response = requests.post(azure_openai_endpoint, headers=headers, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        ai_message = result["choices"][0]["message"]["content"].strip()
                        st.session_state.messages.append({"role": "assistant", "content": ai_message})
                    else:
                        st.error(f"Failed to connect or retrieve response: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"Failed to connect or retrieve response: {str(e)}")

if __name__ == "__main__":
    main()
