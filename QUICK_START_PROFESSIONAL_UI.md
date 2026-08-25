# 🚀 Quick Start Guide - Professional UI

## What's New?

Your Financial Literacy Chatbot now has a **professional, modern user interface** with:
- Modern gradient design and color scheme
- Better organized settings and controls
- Improved chat experience with cleaner layouts
- Professional evaluation dashboard
- Responsive design for all devices

---

## Getting Started

### 1️⃣ **Launch the Application**

```bash
cd e:\Fin-Chat\app
streamlit run chatbot.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 📖 Navigation Guide

### 🌍 **Chatbot Page** (Default)

This is the main interface for interacting with the financial literacy chatbot.

#### Sidebar Options:

**🤖 Model Settings** (Expanded by default)
- Toggle Groq LLM for advanced responses
- Adjust confidence threshold (0.0-1.0)

**📏 Response Settings**
- Set minimum response length in words
- Higher values = more detailed responses

**🎤 Voice Settings**
- Enable/disable voice input via microphone
- Select voice language (English or Chichewa)
- Toggle Text-to-Speech for responses
- Adjust speech speed and volume
- Allow audio file uploads

**🚀 System Control**
- **🔄 Initialize**: Load the RAG system (do this first!)
- **🗑️ Clear**: Clear chat history

**📊 System Status**
- View current system status
- See number of documents loaded
- Check if reranker and translation are active

#### Chat Area:

**Main Panel**
- Your bilingual chatbot interface
- Ask questions in English or Chichewa
- Receive AI-powered responses

**Response Features**
- 🔊 Speak Response: Listen to answers aloud
- 💾 Save Audio: Download responses as audio files
- 📊 Response Details: View confidence, word count, and translation info

---

### 📊 **Evaluation Page**

Test and evaluate your RAG system's performance.

#### Evaluation Settings:

1. **Test Set Size**: Choose how many queries to test (10-100)
2. **Simple Queries**: Use predefined test queries (recommended for quick tests)
3. **Run Evaluation**: Start the evaluation process
4. **Diagnostic**: Quick system health check

#### Results Dashboard:

**📈 Overall Performance**
- BLEU Score: Precision of matches (0-1)
- ROUGE-1, ROUGE-2, ROUGE-L: Recall metrics

**🌍 Performance by Language**
- Separate metrics for English and Chichewa
- Compare language-specific performance

**📁 Performance by Category**
- Performance breakdown by topic category
- Identify weak areas

**⚠️ Problematic Queries**
- See queries with lowest scores
- Identify areas for improvement

**💾 Export Results**
- Download detailed CSV results
- Download JSON summary report

---

## 🎯 First Time Setup

### Step 1: Initialize the System
1. Go to **Chatbot** page
2. Expand **🤖 Model Settings** in sidebar
3. Configure your preferences:
   - Enable Groq LLM (optional)
   - Set confidence threshold
4. Click **🔄 Initialize** button
5. Wait for "✅ System ready!" message

### Step 2: Test Voice (Optional)
1. Expand **🎤 Voice Settings**
2. Check "Enable Voice Input"
3. Select voice language
4. (Optional) Enable Text-to-Speech

### Step 3: Start Chatting
1. Type in the chat input box
2. Or click 🎤 to use voice input
3. Read the response
4. Click 📊 Response Details to see metrics

### Step 4: Run Evaluation (Optional)
1. Go to **📊 Evaluation** page
2. Configure test size (20-50 for quick test)
3. Check "Simple Queries" (faster)
4. Click **🚀 Run**
5. Review the dashboard results

---

## 💡 Pro Tips

### For Best Results:
- **Voice Input**: Speak clearly and naturally
- **Questions**: Ask specific, complete questions
- **English Better**: English questions often get better responses than Chichewa
- **Length Setting**: Increase response length for more detailed answers

### Evaluation Tips:
- **Start Small**: Run with 20 queries first to test
- **Simple Queries**: Use for faster evaluation
- **Check Problematic**: Review low-scoring queries to understand system weaknesses

### Performance Tips:
- Clear chat history before long sessions
- Monitor system status in sidebar
- Use Groq LLM for better quality responses

---

## 🎨 UI Features

### Visual Indicators:
- 🟢 **Green**: System active/ready
- 🔴 **Red**: Errors or issues
- 🟡 **Yellow**: Warnings or inactive components
- ✅ **Check**: Successful operations
- ❌ **Cross**: Failed operations

### Interactive Elements:
- **Expandable Sections**: Click to expand/collapse settings
- **Slider Controls**: Drag to adjust values
- **Tooltips**: Hover over items for help text
- **Progress Bars**: See operation progress
- **Metric Cards**: View key statistics

---

## ⚙️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+L` | Clear sidebar |
| `Ctrl+Shift+K` | Clear script output |
| `r` | Rerun script |
| `e` | Settings menu |

---

## 🔧 Troubleshooting

### "System not initialized"
- Click **🔄 Initialize** in sidebar
- Wait for "✅ System ready!" message
- Check if all files are present in `models/` and `data/` directories

### Voice input not working
- Check browser microphone permissions
- Refresh the page
- Try switching voice language
- Use text input as fallback

### Slow responses
- System might be processing - wait for spinner to complete
- Try enabling Groq LLM for faster responses
- Reduce response length threshold

### Evaluation fails
- Check that system is initialized first
- Try "Simple Queries" option
- Reduce test size
- Check if corpus files are available

---

## 📚 Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| Text Chat | Ask questions in English/Chichewa | ✅ Ready |
| Voice Input | Speak to ask questions | ✅ Ready |
| Text-to-Speech | Listen to responses | ✅ Ready |
| Audio Export | Save responses as audio | ✅ Ready |
| Translation | Auto-translate Chichewa queries | ✅ Ready |
| RAG Retrieval | Smart document search | ✅ Ready |
| Evaluation | Test system performance | ✅ Ready |
| Bilingual Support | English & Chichewa | ✅ Ready |

---

## 📞 Support

If you encounter issues:

1. **Check Sidebar Status**: 
   - Verify all components show green status
   - Check if documents are loaded

2. **Review Documentation**:
   - See `UI_IMPROVEMENTS.md` for design details
   - Check `README.md` for setup instructions

3. **Check Logs**:
   - Look at terminal output for error messages
   - Check browser console (F12) for JavaScript errors

---

## 🎉 You're All Set!

Start chatting with your professional financial literacy chatbot. Enjoy the improved interface!

**Last Updated**: February 2026  
**Version**: 2.0 - Professional UI
