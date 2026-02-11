from flask import Flask, request, jsonify, render_template
import anthropic
import psycopg2
import os



app = Flask(__name__)

# Claude API
client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT', '5432'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        sslmode='require'
    )

def get_all_recipes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.RecipeID, r.RecipeName, r.Description, r.PrepTime, r.CookTime, 
               r.DifficultyLevel, c.CuisineType
        FROM Recipes r
        LEFT JOIN Cuisine c ON r.CuisineID = c.CuisineID
    """)
    recipes = cursor.fetchall()
    conn.close()
    
    # Format recipes for Claude WITH RecipeID
    recipes_text = ""
    for r in recipes:
        recipes_text += f"- [ID:{r[0]}] {r[1]}: {r[2]} ({r[3]+r[4]} min, {r[5]}, {r[6]} cuisine)\n"
    
    return recipes_text

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        # Get recipes from database
        recipes = get_all_recipes()
        
        # Create prompt for Claude
        prompt = f"""You are MunchAI, a friendly and helpful recipe assistant chatbot.

User's request: {user_message}

Available recipes (with IDs):
{recipes}

Your job:
1. Recommend 2-3 recipes that best match what the user wants
2. For EACH recipe you recommend, include a clickable link using this EXACT format:
   [Recipe Name](https://www.recipesvault.org/Recipe/Details/RECIPEID)
   Replace RECIPEID with the actual recipe ID from the list above.
3. Be conversational, warm, and enthusiastic about food
4. Include prep time, difficulty, and cuisine type
5. Keep responses concise but helpful

Example response format:
"I found some great options for you!

1. **[Loaded Omelette](https://www.recipesvault.org/Recipe/Details/5)** - A hearty breakfast option with cheese, bacon, and veggies. Ready in 15 minutes, easy difficulty, American cuisine.

2. **[Veggie Scramble](https://www.recipesvault.org/Recipe/Details/8)** - Lighter option with fresh vegetables. 10 minutes, easy, American cuisine.

Which sounds good to you?"

IMPORTANT: Always include the clickable links in markdown format for every recipe you mention."""

        # Call Claude API
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        bot_response = message.content[0].text
        
        return jsonify({
            'success': True,
            'response': bot_response
        })
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)