import mysql.connector
from tabulate import tabulate
import sys

# ==========================================
# CONFIGURATION
# ==========================================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="cycle@2003",  # <--- CHANGE THIS TO YOUR MYSQL PASSWORD
        database="pantry_chef_db"
    )

# ==========================================
# CORE FUNCTIONS
# ==========================================

def show_pantry():
    """Displays what is currently in your fridge."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # We join with Ingredients table to get the actual NAME, not just the ID
    query = """
    SELECT i.name, p.quantity_available 
    FROM My_Pantry p
    JOIN Ingredients i ON p.ingredient_id = i.ingredient_id
    """
    cursor.execute(query)
    items = cursor.fetchall()
    
    print("\n--- CURRENT PANTRY ---")
    if not items:
        print("Your pantry is empty!")
    else:
        print(tabulate(items, headers=["Ingredient", "Quantity"], tablefmt="grid"))
    
    conn.close()

def add_to_pantry():
    """Adds an item to the pantry. Handles case sensitivity."""
    item_name = input("Enter ingredient name (e.g., Egg): ").strip().title()
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. First, find the ID of this ingredient
        cursor.execute("SELECT ingredient_id FROM Ingredients WHERE name = %s", (item_name,))
        result = cursor.fetchone()

        if result:
            ing_id = result[0]
            # 2. Add to pantry (INSERT IGNORE skips if it already exists to prevent errors)
            cursor.execute("""
                INSERT IGNORE INTO My_Pantry (ingredient_id, quantity_available) 
                VALUES (%s, 'In Stock')
            """, (ing_id,))
            conn.commit()
            print(f"✅ Successfully added {item_name} to pantry.")
        else:
            print(f"❌ Unknown ingredient: '{item_name}'. Please ask admin to add it to the database first.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def find_recipes():
    """
    THE ALGORITHM:
    Finds recipes where the count of MISSING ingredients is ZERO.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # This is the complex Resume-Worthy Query
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

    print("\n--- 🍳 YOU CAN COOK THESE RIGHT NOW 🍳 ---")
    if not recipes:
        print("Nothing! You are missing ingredients for every recipe.")
    else:
        print(tabulate(recipes, headers=["Dish", "Instructions"], tablefmt="fancy_grid"))
    
    conn.close()

def clear_pantry():
    """Helper to wipe pantry for testing"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM My_Pantry")
    conn.commit()
    print("🗑️ Pantry cleared.")
    conn.close()

# ==========================================
# USER INTERFACE LOOP
# ==========================================
def main():
    while True:
        print("\n=== 🧑‍🍳 THE PANTRY CHEF ===")
        print("1. View Pantry")
        print("2. Add Ingredient")
        print("3. What can I cook?")
        print("4. Clear Pantry (Reset)")
        print("5. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            show_pantry()
        elif choice == '2':
            add_to_pantry()
        elif choice == '3':
            find_recipes()
        elif choice == '4':
            clear_pantry()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()