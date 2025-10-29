# 🌙 Somnia - AI-Powered Bedtime Story Generator

Somnia is an intelligent storytelling agent that crafts personalized bedtime stories for children. It leverages advanced LLM technology to analyze user input, ensure content safety, and generate imaginative stories with built-in feedback and evaluation mechanisms.

## ✨ Features

- **Interactive Storytelling Agent**: Automatically understands user prompts and creates tailored bedtime stories
- **Safety-Aware Analyzer**: Detects unsafe, violent, or adult content and responds appropriately to maintain a child-safe experience
- **Dynamic Story Workflow**: Uses an LLM-powered workflow that analyzes, generates, and evaluates stories iteratively
- **Evaluation and Scoring**: Each story is rated for creativity and quality, with feedback to improve storytelling
- **Dual Interface**: Offers both a web interface (Streamlit) and REST API (FastAPI) for flexible usage

## 🛠️ Tools and Technologies

- **Python** - Core programming language
- **LangChain / LangGraph** - LLM orchestration and workflow management
- **GROQ API** - AI model integration
- **Streamlit** - Interactive web interface
- **FastAPI** - RESTful API backend
- **LangSmith** - Tracing and debugging

## 🖼️ App Screenshot

![Somnia Chat Interface](https://ibb.co/C5dZB2jF)
![Somnia Chat Interface](https://ibb.co/FL7My4f4)

## 🔄 How It Works

1. **User Input** → The child or parent enters a story idea or continuation prompt
2. **Analyzer** → Detects intent, name, and ensures content safety
3. **Story Generator** → Crafts a story using an LLM based on the prompt
4. **Evaluator** → Provides feedback and a creativity score
5. **Workflow Loop** → The story improves through multiple iterations if needed

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.8
pip
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/somnia.git
cd somnia

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OpenAI API key to .env
```

### Running the Application

**Streamlit Web Interface:**
```bash
streamlit run app.py
```

**FastAPI Backend:**
```bash
uvicorn api:app --reload
```

## 📋 Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8501`
2. Enter a story prompt or idea
3. Watch as Somnia generates a personalized bedtime story
4. Provide feedback or request story modifications

### API Endpoint
```python
POST /generate-story
{
  "prompt": "A story about a brave little astronaut",
  "child_name": "Emma"
}
```

## 🔮 Future Work

- [ ] Add text-to-speech support for narrated bedtime stories
- [ ] Expand memory for multi-session storytelling
- [ ] Integrate a parental control dashboard for content review
- [ ] Enable multi-language story generation
- [ ] Add illustration generation for visual storytelling
- [ ] Implement user accounts and story history

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions, feedback, or collaboration opportunities:

- **Email**: anikakarampuri04@gmail.com
- **LinkedIn**: [Your Profile](https://www.linkedin.com/in/anika-karampuri-211023260/)
- **GitHub**: [@yourusername](https://github.com/a-k-0209)

## Acknowledgments

- Groq for their powerful language models
- LangChain community for excellent documentation
- All contributors who help make bedtime stories magical

---

Made with ❤️ for children everywhere
