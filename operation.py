from database import get_db_connection
from tabulate import tabulate

def show_pantry():
    conn = get_db_connection()
    if not conn: return

    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.name, p.quantity_available 
        FROM My_Pantry p
        JOIN Ingredients i ON p.ingredient_id = i.ingredient_id
    """)
    items = cursor.fetchall()
    
    print("\n--- CURRENT PANTRY ---")
    if not items:
        print("Your pantry is empty!")
    else:
        print(tabulate(items, headers=["Ingredient", "Quantity"], tablefmt="grid"))
    conn.close()

def add_to_pantry():
    item_name = input("Enter ingredient name: ").strip().title()
    conn = get_db_connection()
    if not conn: return
    
    cursor = conn.cursor()
    # Find ID
    cursor.execute("SELECT ingredient_id FROM Ingredients WHERE name = %s", (item_name,))
    result = cursor.fetchone()

    if result:
        # Insert into Pantry
        cursor.execute("""
            INSERT IGNORE INTO My_Pantry (ingredient_id, quantity_available) 
            VALUES (%s, 'In Stock')
        """, (result[0],))
        conn.commit()
        print(f"✅ Added {item_name}.")
    else:
        print(f"❌ Unknown ingredient: {item_name}")
    conn.close()

def find_recipes():
    conn = get_db_connection()
    if not conn: return
    
    cursor = conn.cursor()
    query = """
    SELECT r.name, r.instructions
    FROM Recipes r
    JOIN Recipe_Ingredients ri ON r.recipe_id = ri.recipe_id
    LEFT JOIN My_Pantry p ON ri.ingredient_id = p.ingredient_id
    GROUP BY r.recipe_id
    HAVING COUNT(CASE WHEN p.ingredient_id IS NULL THEN 1 END) = 0;
    """
    cursor.execute(query)
    recipes = cursor.fetchall()

    print("\n--- 🍳 COOKABLE RECIPES ---")
    if not recipes:
        print("Nothing matches your pantry.")
    else:
        print(tabulate(recipes, headers=["Dish", "Instructions"], tablefmt="fancy_grid"))
    conn.close()

def clear_pantry():
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM My_Pantry")
    conn.commit()
    print("🗑️ Pantry cleared.")
    conn.close()
