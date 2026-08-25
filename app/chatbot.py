# chatbot.py
"""
Main Streamlit application for RAG Financial Literacy Chatbot
Refactored with modular architecture using inheritance and imports
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from config import Config
from chatbot_core import BilingualChatbot
from evaluation import RAGEvaluator
from voice_processor import VoiceProcessor
from audio_utils import AudioHandler, StreamlitAudioHelper
from audio_recording_ui import AudioRecordingUI
from feedback_storage import FeedbackStorage
from faq_search import FAQSearch

# CUSTOM CSS STYLING

def apply_custom_styling():
    """Apply professional custom CSS styling to the application"""
    st.markdown("""
    <style>
    /* Global styling */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #2ca02c;
        --accent-color: #ff7f0e;
        --danger-color: #d62728;
        --warning-color: #ff9800;
        --success-color: #4caf50;
        --background-light: #f8f9fa;
        --background-dark: #0c1223;
        --text-dark: #2c3e50;
        --text-light: #f4f7ff;
        --border-color: #e0e0e0;
        --card-bg: rgba(255, 255, 255, 0.85);
        --card-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }

    /* Page background */
    .stApp {
        background: linear-gradient(135deg, #0d1b3d 0%, #10273e 40%, #111b2b 100%);
        color: var(--text-light);
    }

    /* Hero section */
    .hero {
        padding: 3rem 1rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 18px 40px rgba(0,0,0,0.35);
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }

    .hero h1 {
        margin-bottom: 0.25rem;
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.1;
        color: #ffffff;
    }

    .hero p {
        margin-top: 0;
        margin-bottom: 1.5rem;
        font-size: 1.05rem;
        color: rgba(255,255,255,0.82);
    }

    .hero .search-box {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem;
    }

    .hero .search-box input {
        width: 100%;
        max-width: 720px;
        height: 56px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.25);
        padding: 0 1.2rem;
        font-size: 1.05rem;
        background: rgba(255,255,255,0.12);
        color: #fff;
        outline: none;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }

    .hero .search-box input::placeholder {
        color: rgba(255,255,255,0.65);
    }

    /* Main content cards */
    .section-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: var(--card-shadow);
        margin: 1rem 0;
    }

    .stChatMessage {
        border-radius: 16px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stChatMessage[data-testid="chat-message-user"] {
        background: rgba(29, 185, 84, 0.18);
        border-left: 4px solid rgba(29, 185, 84, 0.75);
    }

    .stChatMessage[data-testid="chat-message-assistant"] {
        background: rgba(83, 99, 214, 0.18);
        border-left: 4px solid rgba(83, 99, 214, 0.75);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 18, 34, 0.95);
        padding: 2rem 1.2rem;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: rgba(255,255,255,0.9);
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: rgba(255,255,255,0.95);
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.9rem;
        font-size: 1.1rem;
    }

    [data-testid="stSidebar"] .stMarkdown h3 {
        border-bottom: 2px solid rgba(255,255,255,0.25);
        padding-bottom: 0.5rem;
    }

    /* Button styling */
    .stButton > button {
        font-weight: 600;
        border-radius: 999px;
        padding: 0.75rem 1.4rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        border: 1px solid rgba(255,255,255,0.16);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(0,0,0,0.3);
    }

    .stButton [kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
    }

    /* Responsive adjustments */
    @media (max-width: 900px) {
        .hero h1 {
            font-size: 2.2rem;
        }

        .hero p {
            font-size: 1rem;
        }

        .hero .search-box input {
            max-width: 100%;
        }

        [data-testid="stSidebar"] {
            padding: 1.2rem;
        }
    }

    @media (max-width: 640px) {
        .main h1 {
            font-size: 2rem;
        }

        .stButton > button {
            width: 100%;
        }

        .stChatMessage {
            padding: 0.9rem;
        }

        .hero {
            padding: 2rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# UI HELPER FUNCTIONS

def show_path_info():
    """Display path information in sidebar"""
    with st.sidebar.expander("📂 Path Information", expanded=False):
        st.write(f"**Script Directory:** {Config.SCRIPT_DIR}")
        st.write(f"**Project Root:** {Config.PROJECT_ROOT}")
        st.write(f"**Models Path:** {Config.MODELS_DIR}")
        st.write(f"**Data Path:** {Config.DATA_DIR}")
        
        st.divider()
        
        path_status = Config.validate_paths()
        
        col1, col2 = st.columns(2)
        with col1:
            status = "✅ Exists" if path_status['models_dir'] else "❌ Missing"
            st.markdown(f"**Models:** {status}")
        with col2:
            status = "✅ Exists" if path_status['data_dir'] else "❌ Missing"
            st.markdown(f"**Data:** {status}")
        
        if path_status['models_dir']:
            model_files = list(Config.MODELS_DIR.glob("*"))
            st.caption(f"📊 Model Files: {len(model_files)} found")
        
        if path_status['data_dir']:
            data_files = list(Config.DATA_DIR.glob("*.pdf"))
            st.caption(f"📄 PDF Files: {len(data_files)} found")


def get_response_length_setting():
    """Get response length setting from sidebar slider"""
    if 'response_length_threshold' not in st.session_state:
        st.session_state.response_length_threshold = Config.DEFAULT_RESPONSE_LENGTH
    
    st.sidebar.subheader("📏 Response Settings")
    response_length_threshold = st.sidebar.slider(
        "Minimum response length (words)",
        min_value=Config.MIN_RESPONSE_LENGTH,
        max_value=Config.MAX_RESPONSE_LENGTH,
        value=st.session_state.response_length_threshold,
        step=10,
        help="Set the minimum number of words required before expansion is triggered.",
        key="response_length_slider"
    )
    
    st.session_state.response_length_threshold = response_length_threshold
    return response_length_threshold

# CHATBOT PAGE

def show_chatbot_page():
    """Display the main chatbot interface"""
    # Apply custom styling
    apply_custom_styling()
    
    # Header section
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.markdown("# 🌍 Financial Literacy Chatbot")
    
    # Language subtitle
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align: center; color: #666; font-size: 0.95rem;'><strong>English</strong></p>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666; font-size: 0.85rem;'>Ask about Financial topics</p>", 
                   unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; color: #666; font-size: 0.95rem;'><strong>Chichewa</strong></p>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666; font-size: 0.85rem;'>Ndufunseni Za Chuma</p>", 
                   unsafe_allow_html=True)
    
    st.divider()
    
    # Sidebar settings
    with st.sidebar:
        st.markdown("## ⚙️ Settings & Configuration")
        
        # Model Settings Tab
        with st.expander("🤖 Model Settings", expanded=True):
            use_groq = st.checkbox(
                "Use Groq LLM", 
                value=False, 
                key="use_groq_checkbox",
                help="Enable advanced language model for better responses"
            )
            confidence_threshold = st.slider(
                "Confidence Threshold", 
                0.0, 1.0, Config.DEFAULT_CONFIDENCE_THRESHOLD, 0.01,
                key="confidence_threshold_slider",
                help="Minimum confidence level for responses"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"📊 Min: {0.0}")
            with col2:
                st.caption(f"Max: {1.0}")
        
        # Response Length Settings
        with st.expander("📏 Response Settings", expanded=False):
            response_length_threshold = st.slider(
                "Minimum Response Length",
                min_value=Config.MIN_RESPONSE_LENGTH,
                max_value=Config.MAX_RESPONSE_LENGTH,
                value=st.session_state.get('response_length_threshold', Config.DEFAULT_RESPONSE_LENGTH),
                step=10,
                help="Set the minimum number of words required before expansion is triggered",
                key="response_length_slider"
            )
            st.session_state.response_length_threshold = response_length_threshold
        
        # Voice Input Settings
        with st.expander("🎤 Voice Settings", expanded=False):
            enable_voice = st.checkbox(
                "Enable Voice Input",
                value=Config.VOICE_INPUT_ENABLED_BY_DEFAULT,
                key="enable_voice_checkbox",
                help="Allow input via microphone"
            )
            
            if enable_voice:
                voice_language = st.selectbox(
                    "Voice Input Language",
                    options=list(Config.VOICE_LANGUAGES.keys()),
                    format_func=lambda x: Config.VOICE_LANGUAGES[x],
                    key="voice_language_selectbox"
                )
                
                enable_tts = st.checkbox(
                    "Enable Text-to-Speech",
                    value=Config.ENABLE_TEXT_TO_SPEECH,
                    key="enable_tts_checkbox",
                    help="Speak chatbot responses aloud"
                )
                
                if enable_tts:
                    col1, col2 = st.columns(2)
                    with col1:
                        tts_speed = st.slider(
                            "Speech Speed",
                            min_value=50,
                            max_value=300,
                            value=Config.TTS_VOICE_RATE,
                            step=10,
                            key="tts_speed_slider",
                            help="Words per minute"
                        )
                    with col2:
                        tts_volume = st.slider(
                            "Volume",
                            min_value=0.0,
                            max_value=1.0,
                            value=Config.TTS_VOLUME,
                            step=0.1,
                            key="tts_volume_slider"
                        )
                
                allow_file_upload = st.checkbox(
                    "Allow Audio File Upload",
                    value=Config.ALLOW_AUDIO_FILE_UPLOAD,
                    key="allow_audio_upload_checkbox",
                    help="Upload pre-recorded audio files"
                )
        
        # Get API key
        groq_key = Config.get_groq_api_key()
        
        st.divider()
        
        # System Control Buttons
        st.markdown("### 🚀 System Control")
        
        col1, col2 = st.columns(2)
        with col1:
            init_btn = st.button(
                "🔄 Initialize", 
                type="primary", 
                use_container_width=True, 
                key="init_button",
                help="Load RAG system"
            )
        with col2:
            clear_btn = st.button(
                "🗑️ Clear", 
                use_container_width=True, 
                key="clear_chat_button",
                help="Clear chat history"
            )
        
        if init_btn:
            with st.spinner("⏳ Loading RAG system..."):
                try:
                    chatbot = BilingualChatbot()
                    api_key = groq_key if use_groq else None
                    if chatbot.initialize(groq_api_key=api_key):
                        chatbot.response_length_threshold = response_length_threshold
                        st.session_state.chatbot = chatbot
                        st.session_state.system_ready = True
                        st.success("✅ System ready!")
                        st.balloons()
                    else:
                        st.error("❌ Initialization failed")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    import traceback
                    st.error(traceback.format_exc())
        
        if clear_btn:
            st.session_state.messages = []
            st.success("✅ Chat cleared!")
            st.rerun()
        
        st.divider()
        
        # System Status
        st.markdown("### 📊 System Status")
        if st.session_state.system_ready and st.session_state.chatbot:
            info = st.session_state.chatbot.get_system_info()
            
            # Status indicator
            status_color = "🟢" if info['status'] == 'ready' else "🔴"
            st.markdown(f"{status_color} **Status:** {info['status'].upper()}")
            
            # Metrics in columns
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📚 Documents", info['documents_count'])
            with col2:
                st.metric("🎯 Reranker", "Active" if info['reranker_enabled'] else "Inactive")
            
            # Component status
            with st.expander("📋 Component Details", expanded=False):
                comp_col1, comp_col2 = st.columns(2)
                
                with comp_col1:
                    if info['llm_enabled']:
                        st.success("✅ LLM: Active")
                    else:
                        st.warning("⚠️ LLM: Disabled")
                
                with comp_col2:
                    if info.get('translation_enabled'):
                        st.success("✅ Translation: Ready")
                    else:
                        st.info("ℹ️ Translation: Not available")
        else:
            st.warning("⚠️ System not initialized")
            st.info("👆 Click 'Initialize' to start", icon="ℹ️")
        
        # Feedback Stats
        st.divider()
        st.markdown("### 📊 Feedback Stats")
        
        if st.session_state.system_ready:
            stats = st.session_state.feedback_storage.get_feedback_stats()
            
            if stats['total_responses'] > 0:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("👍 Helpful", f"{stats['positive']}")
                with col2:
                    st.metric("👎 Not Helpful", f"{stats['negative']}")
                
                # Helpfulness rate
                helpfulness = stats['helpfulness_rate']
                if helpfulness >= 80:
                    st.success(f"🎉 {helpfulness:.1f}% helpful")
                elif helpfulness >= 60:
                    st.warning(f"⚠️ {helpfulness:.1f}% helpful")
                else:
                    st.error(f"❌ {helpfulness:.1f}% helpful")
            else:
                st.info("No feedback yet")
        else:
            st.info("Initialize system to view feedback stats")
        
        # FAQ Search
        st.divider()
        st.markdown("### 🔍 FAQ Search")
        
        if st.session_state.system_ready:
            # Initialize FAQ search if not already done
            if 'faq_search' not in st.session_state:
                from faq_search import FAQSearch
                st.session_state.faq_search = FAQSearch(st.session_state.chatbot.rag_retriever)
            
            # Search input
            search_query = st.text_input(
                "Search FAQs",
                placeholder="Ask about financial topics...",
                key="faq_search_input",
                help="Search through financial literacy FAQs"
            )
            
            if search_query:
                with st.spinner("🔍 Searching FAQs..."):
                    search_results = st.session_state.faq_search.search_faqs(search_query, top_k=5)
                
                if search_results.get('error'):
                    st.error(f"Search error: {search_results['error']}")
                elif search_results['results']:
                    st.markdown(f"**Found {len(search_results['results'])} relevant FAQs:**")
                    
                    # Display results
                    for i, result in enumerate(search_results['results'], 1):
                        with st.expander(f"#{i} {result['question'][:60]}{'...' if len(result['question']) > 60 else ''}", expanded=i<=2):
                            st.markdown(f"**Question:** {result['question']}")
                            st.markdown(f"**Answer:** {result['answer']}")
                            
                            # Metadata
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.caption(f"📊 Confidence: {result['confidence']:.1f}%")
                            with col2:
                                st.caption(f"🌍 Language: {result['language']}")
                            with col3:
                                st.caption(f"📁 Category: {result['category']}")
                    
                    # People Also Asked
                    if search_results.get('people_also_asked'):
                        st.divider()
                        st.markdown("### 👥 People Also Asked")
                        
                        for suggestion in search_results['people_also_asked'][:5]:
                            if st.button(
                                f"🔍 {suggestion}",
                                key=f"suggestion_{hash(suggestion)}",
                                help="Click to search this question",
                                use_container_width=True
                            ):
                                # This will trigger a rerun with the new search
                                st.session_state.faq_search_input = suggestion
                                st.rerun()
                else:
                    st.info("No relevant FAQs found. Try rephrasing your question.")
            
            # Search stats
            search_stats = st.session_state.faq_search.get_search_stats()
            if search_stats['total_searches'] > 0:
                with st.expander("📈 Search Statistics", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Searches", search_stats['total_searches'])
                    with col2:
                        st.metric("Unique Queries", search_stats['unique_queries'])
                    
                    if search_stats['popular_searches']:
                        st.markdown("**Popular Searches:**")
                        for search in search_stats['popular_searches'][:3]:
                            st.caption(f"• {search}")
        else:
            st.info("Initialize system to search FAQs")
        
        # Footer
        st.divider()
        st.caption("💡 Tip: Use voice input for hands-free interaction")
    
    # Main Chat Area
    st.markdown("## 💬 Chat Interface")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Input area
    st.divider()
    st.markdown("### 💭 Your Message")
    
    prompt = None

    # Check for voice input first
    if not prompt and st.session_state.get('voice_input'):
        prompt = st.session_state.voice_input
        st.session_state.voice_input = None
    else:
        # Use inline microphone button if voice enabled
        enable_voice_input = st.session_state.get('enable_voice_checkbox', False)
        if not prompt:
            if enable_voice_input:
                voice_language = st.session_state.get('voice_language_selectbox', 'en-US')
                prompt = AudioRecordingUI.render_chat_input_with_microphone(
                    enable_voice=True,
                    voice_language=voice_language,
                    placeholder="💬 Ask about financial topics... or 🎤 to speak"
                )
            else:
                prompt = st.chat_input("💬 Ask about financial topics...")
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        if st.session_state.system_ready:
            with st.chat_message("assistant"):
                with st.spinner("🔍 Processing with RAG pipeline..."):
                    result = st.session_state.chatbot.process_query(
                        prompt, 
                        confidence_threshold=confidence_threshold
                    )
                
                # Display answer
                st.markdown(result['answer'])
                
                # Response Actions
                st.divider()
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    # Text-to-speech output
                    if st.session_state.get('enable_tts_checkbox', False):
                        if st.button(
                            "🔊 Speak Response",
                            key=f"speak_response_{len(st.session_state.messages)}",
                            use_container_width=True
                        ):
                            try:
                                with st.spinner("🔊 Speaking..."):
                                    voice_processor = VoiceProcessor(enable_tts=True)
                                    voice_processor.set_language(st.session_state.get('voice_language_selectbox', 'en-US'))
                                    
                                    if voice_processor.tts:
                                        voice_processor.tts.voice_rate = st.session_state.get('tts_speed_slider', Config.TTS_VOICE_RATE)
                                        voice_processor.tts.volume = st.session_state.get('tts_volume_slider', Config.TTS_VOLUME)
                                    
                                    success = voice_processor.speak_response(result['answer'])
                                    
                                    if success:
                                        st.success("✅ Response spoken")
                                    else:
                                        st.warning("⚠️ Text-to-speech unavailable")
                            except Exception as e:
                                st.warning(f"⚠️ TTS error: {str(e)}")
                
                with col2:
                    if st.button("💾", key=f"save_audio_{len(st.session_state.messages)}", help="Save as audio file", use_container_width=True):
                        try:
                            Config.TTS_TEMP_DIR.mkdir(exist_ok=True)
                            audio_file = Config.TTS_TEMP_DIR / f"response_{len(st.session_state.messages)}.wav"
                            
                            voice_processor = VoiceProcessor(enable_tts=True)
                            success = voice_processor.speak_response_to_file(str(result['answer']), str(audio_file))
                            
                            if success:
                                st.success("✅ Audio saved")
                            else:
                                st.error("❌ Failed to save audio")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                
                with col3:
                    st.empty()  # Placeholder for alignment
                
                # Show word count info
                word_count = result.get('word_count', 0)
                threshold_met = word_count >= response_length_threshold
                status_emoji = "✅" if threshold_met else "⚠️"
                
                st.caption(
                    f"{status_emoji} Response: {word_count} words (threshold: {response_length_threshold})"
                )
                
                # Show metadata in expander
                with st.expander("📊 Response Details", expanded=False):
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    with metric_col1:
                        st.metric("Type", result['response_type'])
                    with metric_col2:
                        st.metric("Confidence", f"{result['confidence']:.2%}")
                    with metric_col3:
                        threshold_emoji = "✅" if result.get('threshold_met') else "⚠️"
                        st.metric("Threshold", f"{threshold_emoji}")
                    with metric_col4:
                        st.metric("Words", word_count)
                    
                    st.divider()
                    
                    # Translation info
                    if result.get('translated'):
                        st.success(f"🌍 Answer translated to {result.get('language', 'target language')}")
                        st.caption(f"Original language: {result.get('query_language', 'unknown').upper()}")
                        
                        if result.get('original_answer'):
                            with st.expander("📝 Original English Version"):
                                st.write(result['original_answer'][:300] + "...")
                    else:
                        st.info("📄 Direct response (no translation needed)")
                
                # Feedback System
                st.divider()
                st.markdown("### 💬 Was this response helpful?")
                st.markdown('<div class="feedback-buttons">', unsafe_allow_html=True)
                feedback_col1, feedback_col2 = st.columns(2)
                
                with feedback_col1:
                    if st.button(
                        "👍 Yes, helpful", 
                        key=f"feedback_positive_{len(st.session_state.messages)}",
                        use_container_width=True,
                        help="Mark this response as helpful"
                    ):
                        success = st.session_state.feedback_storage.save_feedback(
                            query=prompt,
                            response=result['answer'],
                            feedback='positive',
                            confidence=result.get('confidence')
                        )
                        if success:
                            st.success("✅ Thanks for your feedback!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save feedback")
                
                with feedback_col2:
                    if st.button(
                        "👎 Not helpful", 
                        key=f"feedback_negative_{len(st.session_state.messages)}",
                        use_container_width=True,
                        help="Mark this response as not helpful"
                    ):
                        success = st.session_state.feedback_storage.save_feedback(
                            query=prompt,
                            response=result['answer'],
                            feedback='negative',
                            confidence=result.get('confidence')
                        )
                        if success:
                            st.success("✅ Thanks for your feedback!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save feedback")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result['answer']
                })
        else:
            st.warning("⚠️ System not initialized. Please click 'Initialize' in the sidebar first.", icon="⚠️")


# ============================================================================
# EVALUATION PAGE
# ============================================================================

def show_evaluation_page():
    """Display the evaluation dashboard"""
    # Apply custom styling
    apply_custom_styling()
    
    st.markdown("# 📊 RAG System Evaluation Dashboard")
    
    if not st.session_state.system_ready:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.warning("⚠️ RAG system not initialized", icon="⚠️")
        with col2:
            st.info("👈 Initialize on Chatbot page", icon="ℹ️")
        return
    
    st.markdown("""
    ---
    **Evaluate your RAG system's performance using standard metrics:**
    - 📈 **BLEU Score**: Measures precision of n-gram matches (0-1)
    - 📊 **ROUGE Scores**: Measures recall of n-gram matches (ROUGE-1, ROUGE-2, ROUGE-L)
    """)
    
    st.divider()
    
    # Evaluation controls
    st.markdown("### ⚙️ Evaluation Settings")
    
    col1, col2, col3 = st.columns([2, 1.5, 2])
    
    with col1:
        test_size = st.slider(
            "Test Set Size", 
            10, 100, 20, 5,
            key="test_size_slider_evaluation",
            help="Number of test queries to evaluate"
        )
    with col2:
        use_simple_queries = st.checkbox(
            "Simple Queries",
            value=True,
            help="Use predefined test queries",
            key="use_simple_queries_checkbox"
        )
    with col3:
        col3a, col3b = st.columns(2)
        with col3a:
            run_eval = st.button(
                "🚀 Run", 
                type="primary", 
                use_container_width=True,
                key="run_eval_button_evaluation"
            )
        with col3b:
            diagnostic = st.button(
                "🔍 Diagnostic", 
                use_container_width=True,
                key="diagnostic_button"
            )
    
    st.divider()
    
    # Run evaluation
    if run_eval or 'eval_results' in st.session_state:
        if run_eval:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner("🔍 Running evaluation..."):
                try:
                    status_text.text("Initializing evaluator...")
                    progress_bar.progress(20)
                    
                    evaluator = RAGEvaluator(
                        st.session_state.chatbot.rag_retriever
                    )
                    
                    if use_simple_queries:
                        status_text.text("Loading test queries...")
                        progress_bar.progress(40)
                        test_cases = evaluator.create_simple_test_queries(test_size)
                    else:
                        status_text.text("Creating test cases from corpus...")
                        progress_bar.progress(40)
                        test_cases = evaluator.create_test_set(
                            st.session_state.chatbot.rag_retriever.corpus_metadata,
                            samples_per_category=max(3, test_size // 10)
                        )[:test_size]
                    
                    if not test_cases:
                        st.error("❌ No test cases could be created. Check your corpus data.")
                        return
                    
                    status_text.text("Evaluating responses...")
                    progress_bar.progress(60)
                    
                    results_df = evaluator.run_evaluation(test_cases)
                    
                    status_text.text("Generating report...")
                    progress_bar.progress(80)
                    
                    report = evaluator.generate_report(results_df)
                    
                    st.session_state.eval_results = results_df
                    st.session_state.eval_report = report
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    st.success(f"✅ Evaluation complete! Tested {len(test_cases)} queries")
                    
                except Exception as e:
                    st.error(f"❌ Evaluation failed: {e}")
                    import traceback
                    st.error(traceback.format_exc())
                    return
        
        # Display results
        results_df = st.session_state.get('eval_results', pd.DataFrame())
        report = st.session_state.get('eval_report', {})
        
        if not report or 'overall' not in report or not report['overall']:
            st.warning("⚠️ No evaluation results available.", icon="⚠️")
            return
        
        overall = report.get('overall', {})
        
        # Overall metrics
        st.markdown("## 📈 Overall Performance")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            bleu = overall.get('bleu', 0.0)
            st.metric("BLEU Score", f"{bleu:.3f}", f"{bleu*100:.1f}%")
        with metric_col2:
            rouge1 = overall.get('rouge1', 0.0)
            st.metric("ROUGE-1", f"{rouge1:.3f}", f"{rouge1*100:.1f}%")
        with metric_col3:
            rouge2 = overall.get('rouge2', 0.0)
            st.metric("ROUGE-2", f"{rouge2:.3f}", f"{rouge2*100:.1f}%")
        with metric_col4:
            rougeL = overall.get('rougeL', 0.0)
            st.metric("ROUGE-L", f"{rougeL:.3f}", f"{rougeL*100:.1f}%")
        
        st.divider()
        
        # Language performance
        st.markdown("## 🌍 Performance by Language")
        lang_data = report.get('by_language', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown("### 🇬🇧 English")
                if 'English' in lang_data:
                    en = lang_data['English']
                    lang_col1, lang_col2 = st.columns(2)
                    with lang_col1:
                        st.metric("Queries", en.get('count', 0))
                        st.metric("BLEU", f"{en.get('bleu', 0.0):.3f}")
                    with lang_col2:
                        st.metric("ROUGE-1", f"{en.get('rouge1', 0.0):.3f}")
                        st.metric("ROUGE-L", f"{en.get('rougeL', 0.0):.3f}")
                else:
                    st.info("No data available")
        
        with col2:
            with st.container():
                st.markdown("### 🇲🇼 Chichewa")
                if 'Chichewa' in lang_data:
                    ny = lang_data['Chichewa']
                    lang_col1, lang_col2 = st.columns(2)
                    with lang_col1:
                        st.metric("Queries", ny.get('count', 0))
                        st.metric("BLEU", f"{ny.get('bleu', 0.0):.3f}")
                    with lang_col2:
                        st.metric("ROUGE-1", f"{ny.get('rouge1', 0.0):.3f}")
                        st.metric("ROUGE-L", f"{ny.get('rougeL', 0.0):.3f}")
                else:
                    st.info("No data available")
        
        st.divider()
        
        # Category performance
        st.markdown("## 📁 Performance by Category")
        cat_data = report.get('by_category', {})
        
        if cat_data:
            cat_df = pd.DataFrame([
                {
                    'Category': cat,
                    'Queries': metrics.get('count', 0),
                    'BLEU': f"{metrics.get('bleu', 0.0):.3f}",
                    'ROUGE-1': f"{metrics.get('rouge1', 0.0):.3f}",
                    'ROUGE-2': f"{metrics.get('rouge2', 0.0):.3f}",
                    'ROUGE-L': f"{metrics.get('rougeL', 0.0):.3f}"
                }
                for cat, metrics in cat_data.items()
            ])
            
            st.dataframe(cat_df, use_container_width=True, hide_index=True)
        else:
            st.info("No category data available")
        
        st.divider()
        
        # Problematic queries
        st.markdown("## ⚠️ Problematic Queries")
        st.caption("Queries with lowest BLEU scores:")
        
        prob_queries = report.get('problematic_queries', [])[:10]
        
        if prob_queries:
            prob_df = pd.DataFrame([
                {
                    'Query': pq.get('query', 'N/A')[:50] + "...",
                    'Language': pq.get('language', 'N/A'),
                    'Category': pq.get('category', 'N/A'),
                    'BLEU': f"{pq.get('bleu', 0.0):.3f}",
                    'ROUGE-L': f"{pq.get('rougeL', 0.0):.3f}"
                }
                for pq in prob_queries
            ])
            
            st.dataframe(prob_df, use_container_width=True, hide_index=True)
        else:
            st.info("No problematic queries to display")
        
        st.divider()
        
        # Export results
        st.markdown("## 💾 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not results_df.empty:
                csv = results_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 CSV Results",
                    data=csv,
                    file_name="rag_evaluation_results.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_csv_evaluation"
                )
            else:
                st.button(
                    "📥 CSV Results",
                    disabled=True,
                    use_container_width=True,
                    key="download_csv_disabled_evaluation"
                )
        
        with col2:
            if report:
                import json
                report_json = json.dumps(report, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📥 JSON Report",
                    data=report_json,
                    file_name="rag_evaluation_report.json",
                    mime="application/json",
                    use_container_width=True,
                    key="download_json_evaluation"
                )
            else:
                st.button(
                    "📥 JSON Report",
                    disabled=True,
                    use_container_width=True,
                    key="download_json_disabled_evaluation"
                )
    
    # Diagnostic section
    if diagnostic:
        st.divider()
        st.markdown("## 🔧 Diagnostic Analysis")
        
        with st.spinner("Running diagnostic..."):
            try:
                evaluator = RAGEvaluator(st.session_state.chatbot.rag_retriever)
                diagnostic_result = evaluator.run_diagnostic()
                
                diag_col1, diag_col2, diag_col3, diag_col4 = st.columns(4)
                
                with diag_col1:
                    st.metric("BLEU Score", f"{diagnostic_result['bleu']:.3f}")
                with diag_col2:
                    st.metric("ROUGE-L Score", f"{diagnostic_result['rougeL']:.3f}")
                with diag_col3:
                    st.metric("Answer Length", diagnostic_result['answer_length'])
                with diag_col4:
                    st.metric("Status", "✅ OK")
                
                with st.expander("📝 Generated Answer"):
                    st.write(diagnostic_result['generated_answer'])
            
            except Exception as e:
                st.error(f"❌ Diagnostic failed: {e}")
# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main Streamlit application entry point"""
    st.set_page_config(
        page_title="Financial Literacy Chatbot",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Add viewport meta tag for mobile responsiveness
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, unsafe_allow_html=True)
    
    # Apply custom styling at startup
    apply_custom_styling()
    
    # Initialize session state
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'system_ready' not in st.session_state:
        st.session_state.system_ready = False
    if 'voice_input' not in st.session_state:
        st.session_state.voice_input = None
    if 'show_recording' not in st.session_state:
        st.session_state.show_recording = False
    if 'show_upload' not in st.session_state:
        st.session_state.show_upload = False
    if 'enable_voice' not in st.session_state:
        st.session_state.enable_voice = Config.VOICE_INPUT_ENABLED_BY_DEFAULT
    if 'response_length_threshold' not in st.session_state:
        st.session_state.response_length_threshold = Config.DEFAULT_RESPONSE_LENGTH
    if 'feedback_storage' not in st.session_state:
        st.session_state.feedback_storage = FeedbackStorage()
    
    # Page navigation
    page = st.sidebar.radio(
        "📍 Navigation",
        ["💬 Chatbot", "📊 Evaluation"],
        index=0,
        key="navigation_radio"
    )
    
    # Route to appropriate page
    if page == "💬 Chatbot":
        show_chatbot_page()
    elif page == "📊 Evaluation":
        show_evaluation_page()


if __name__ == "__main__":
    main()
