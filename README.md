# MunchAI

An AI-powered recipe chatbot using Retrieval-Augmented Generation (RAG) architecture to provide intelligent, data-backed recipe recommendations and cooking assistance.

[![Live Demo](https://img.shields.io/badge/Demo-munchai.org-green)](https://www.munchai.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Project Overview

MunchAI is a conversational AI service built with Python Flask that serves as the intelligent backend for the Recipe Vault ecosystem. It demonstrates enterprise-level AI integration patterns by implementing a RAG architecture that grounds AI responses in verified database information, preventing hallucinations and ensuring reliable recommendations.

The chatbot provides natural language recipe search, ingredient substitution suggestions, cooking technique explanations, dietary restriction filtering, and nutritional information queries - all backed by a PostgreSQL database containing 280+ ingredients and 50+ curated recipes.

### Key Features

- **RAG Architecture** - Database-first approach that queries structured data before AI generation
- **Claude API Integration** - Leverages Anthropic's Claude for natural language understanding
- **Real-time Recipe Search** - Conversational interface for finding recipes based on ingredients, cuisine, or dietary needs
- **Ingredient Substitutions** - AI-powered suggestions for ingredient alternatives
- **Cooking Assistance** - Step-by-step guidance and technique explanations
- **Dietary Filtering** - Support for vegetarian, vegan, gluten-free, and other dietary restrictions
- **PostgreSQL Backend** - Shared database with Recipe Vault for consistent data

## Integration

MunchAI serves as the AI backend for [Recipe Vault](https://github.com/hrashid13/recipe-vault), a full-stack recipe management application built with ASP.NET Core. Together, they form a comprehensive recipe ecosystem that combines traditional CRUD operations with modern AI-powered assistance.

## Architecture

### RAG Implementation

The "database first, AI second" approach prevents AI hallucinations and ensures grounded responses:

1. **User Query Processing** - Natural language input parsed for intent and entities
2. **Database Retrieval** - SQL queries fetch relevant recipes, ingredients, and cooking data
3. **Context Assembly** - Retrieved data structured into coherent context
4. **AI Generation** - Context sent to Claude API with engineered prompts
5. **Response Delivery** - Natural language response generated from verified data only

### Tech Stack

**Backend:**
- Python 3.9+
- Flask (Web Framework)
- psycopg2 (PostgreSQL Driver)
- Anthropic SDK (Claude API)

**Database:**
- PostgreSQL 14+
- Shared schema with Recipe Vault

**AI/ML:**
- Claude API (Anthropic)
- Custom prompt engineering
- Context window management

**Deployment:**
- Railway (Hosting)
- Custom Domain Configuration
- Environment-based configuration

### System Design

```
User Query
    ↓
Flask API Endpoint
    ↓
Query Parser → Extract Intent & Entities
    ↓
Database Layer → PostgreSQL Query
    ↓
Context Builder → Structure Retrieved Data
    ↓
Claude API → Generate Natural Language Response
    ↓
Response Handler → Format & Return
```

## Database Schema

MunchAI shares the Recipe Vault database schema:

- `Recipes` - Recipe metadata and cooking information
- `Ingredients` - Comprehensive ingredient catalog (280+ items)
- `RecipeIngredients` - Recipe-ingredient relationships with quantities
- `Instructions` - Step-by-step cooking instructions
- `Tags` - Recipe categorization (vegetarian, quick meals, etc.)
- `Cuisine` - Cultural cuisine classifications
- `Units` - Measurement units for ingredients
- `Category` - Ingredient categorization (28+ categories)

## Getting Started

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 14+
- Claude API key from Anthropic
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/hrashid13/munchai.git
cd munchai
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your credentials:
# DATABASE_URL=postgresql://username:password@localhost:5432/RecipeVaultDB
# CLAUDE_API_KEY=your_claude_api_key_here
# FLASK_SECRET_KEY=your_secret_key_here
```

5. **Initialize database** (if not already done via Recipe Vault)
```bash
# Database should already exist from Recipe Vault setup
# MunchAI connects to the same PostgreSQL database
```

6. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Configuration

Create a `.env` file with the following variables:

```
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/RecipeVaultDB

# Claude API Configuration
CLAUDE_API_KEY=your_anthropic_api_key

# Flask Configuration
FLASK_SECRET_KEY=your_random_secret_key
FLASK_ENV=development
FLASK_DEBUG=True

# Application Settings
MAX_CONTEXT_LENGTH=4000
TEMPERATURE=0.7
```

## API Endpoints

### Chat Endpoint
```
POST /chat
Content-Type: application/json

{
  "message": "Find me a vegetarian pasta recipe",
  "conversation_id": "optional-session-id"
}

Response:
{
  "response": "I found several vegetarian pasta recipes...",
  "recipes": [...],
  "conversation_id": "session-id"
}
```

### Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "database": "connected",
  "ai_service": "available"
}
```

## Project Structure

```
munchai/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── routes/
│   ├── chat.py               # Chat endpoint handlers
│   └── health.py             # Health check endpoints
├── services/
│   ├── rag_service.py        # RAG implementation
│   ├── database_service.py   # Database queries
│   ├── claude_service.py     # Claude API integration
│   └── prompt_builder.py     # Prompt engineering
├── models/
│   └── conversation.py       # Conversation state management
└── utils/
    ├── query_parser.py       # Natural language parsing
    └── response_formatter.py # Response formatting
```

## RAG Architecture Deep Dive

### Query Processing Pipeline

1. **Intent Classification**
   - Recipe search
   - Ingredient substitution
   - Cooking technique
   - Nutritional information

2. **Entity Extraction**
   - Ingredients mentioned
   - Cuisine preferences
   - Dietary restrictions
   - Cooking methods

3. **Database Query Construction**
   - Dynamic SQL generation based on extracted entities
   - Joins across recipe, ingredient, and instruction tables
   - Filtering by tags, cuisine, difficulty

4. **Context Assembly**
   - Structured format for Claude API
   - Include recipe details, ingredients, instructions
   - Add relevant metadata (prep time, servings, etc.)

5. **Prompt Engineering**
   - System prompts for role definition
   - Context injection with retrieved data
   - Output format specifications

### Example RAG Flow

**User:** "What can I make with chicken and rice?"

1. **Parse:** Extract ingredients (chicken, rice)
2. **Query:** `SELECT * FROM Recipes JOIN RecipeIngredients WHERE ingredient IN ('chicken', 'rice')`
3. **Retrieve:** Found 5 matching recipes
4. **Format Context:**
```
You are a helpful cooking assistant. Based on the following recipes from our database:

Recipe 1: Chicken Fried Rice
- Ingredients: chicken breast, rice, soy sauce, eggs...
- Instructions: 1. Cook rice... 2. Stir fry chicken...

Recipe 2: Chicken Biryani
...
```
5. **Generate:** Claude produces natural language response recommending recipes
6. **Return:** User receives conversational response with recipe suggestions

## Performance Optimizations

- **Connection Pooling** - Efficient database connection management
- **Query Caching** - Cache frequent ingredient/recipe lookups
- **Context Pruning** - Limit context to relevant information only
- **Async Processing** - Non-blocking I/O for Claude API calls
- **Response Streaming** - Stream AI responses for faster perceived performance

## Security

- Environment-based configuration for secrets
- SQL injection prevention via parameterized queries
- Rate limiting on API endpoints
- CORS configuration for frontend integration
- API key validation and rotation support

## Deployment

### Railway Deployment

1. **Connect GitHub repository**
2. **Configure environment variables** in Railway dashboard
3. **Deploy**
4. **Configure custom domain** (munchai.org)

Environment variables required:
- `DATABASE_URL`
- `CLAUDE_API_KEY`
- `FLASK_SECRET_KEY`

### Production Considerations

- Use production-grade WSGI server (Gunicorn)
- Enable HTTPS via Railway
- Configure database connection pooling
- Set up monitoring and logging
- Implement rate limiting
- Configure CORS for Recipe Vault domain

## Learning Outcomes

This project demonstrates proficiency in:

- **AI Integration** - Implementing RAG architecture for enterprise applications
- **API Development** - RESTful API design with Flask
- **Database Design** - Complex queries and relationship management
- **Prompt Engineering** - Effective communication with LLMs
- **Cloud Deployment** - Production deployment on Railway
- **System Architecture** - Microservices and service-oriented design
- **Python Development** - Modern Python practices and package management

## Use Cases Beyond Recipes

The RAG architecture pattern demonstrated in MunchAI is directly applicable to:

- **Healthcare AI** - Patient data retrieval + AI-powered diagnosis assistance
- **Customer Service** - Knowledge base search + conversational support
- **Legal Tech** - Case law retrieval + AI-powered legal analysis
- **E-commerce** - Product catalog search + personalized recommendations
- **Education** - Curriculum content retrieval + AI tutoring

This implementation showcases enterprise-level patterns for building reliable, data-backed conversational AI systems.

## Future Enhancements

- **Multi-language Support** - Recipe recommendations in multiple languages
- **Voice Interface** - Voice-to-text for hands-free cooking
- **Image Recognition** - Upload ingredient photos for identification
- **Meal Planning Integration** - AI-powered weekly meal plan generation
- **Nutritional Analysis** - Detailed macronutrient breakdowns
- **User Preferences** - Personalized recommendations based on history
- **Recipe Scaling** - Automatic ingredient quantity adjustments

## Contributing

This is a portfolio project, but feedback and suggestions are welcome. Please open an issue to discuss potential improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Hesham Rashid**
- Portfolio: https://www.heshamrashid.org/
- LinkedIn: https://www.linkedin.com/in/hesham-rashid/
- Email: h.f.rashid@gmail.com

Master's in AI and Business Analytics - University of South Florida

## Related Projects

- [Recipe Vault](https://github.com/hrashid13/recipe-vault) - Full-stack recipe management application (ASP.NET Core)

## Acknowledgments

- Anthropic for Claude API
- Flask framework community
- PostgreSQL database
- Railway hosting platform

## Contact

For questions, collaboration opportunities, or career inquiries, please reach out via h.f.rashid@gmail.com or LinkedIn.

---

**Note**: This project demonstrates practical implementation of RAG architecture for conversational AI. The patterns and techniques used here are directly applicable to healthcare AI systems, customer service chatbots, legal tech applications, and other enterprise domains requiring reliable, data-backed AI responses.
