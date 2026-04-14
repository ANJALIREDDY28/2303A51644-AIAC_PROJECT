import random
from typing import Dict

def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m ** 2), 1)

def calculate_bmr(gender, weight, height, age):
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_calories(bmr, activity, goal):
    activity_map = {"low": 1.2, "medium": 1.55, "high": 1.9}
    calories = bmr * activity_map.get(activity.lower(), 1.55)
    if goal == "weight_loss":
        calories -= 400
    elif goal == "weight_gain":
        calories += 400
    return int(calories)

def generate_diet_plan(data: Dict) -> Dict:
    random.seed()  # Ensure randomness
    age = int(data.get('age', 25))
    gender = data.get('gender', 'male').lower()
    height = float(data.get('height', 170))
    weight = float(data.get('weight', 70))
    activity = data.get('activity_level', 'medium').lower()
    goal = data.get('goal', 'maintenance').lower()
    preference = data.get('food_preference', 'veg').lower()
    
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(gender, weight, height, age)
    calories = calculate_calories(bmr, activity, goal)
    
    water = int(weight * 35)
    
    # Calorie level
    if calories < 1800:
        level = "low"
    elif calories < 2600:
        level = "medium"
    else:
        level = "high"
    
    # EXPANDED FOOD DATABASE (10+ per category)
    veg_meals = {
        'low': {
            'breakfast': ['Oats porridge', 'Fruits & nuts bowl', 'Idli sambar', 'Moong dal chilla', 'Veg sandwich', 'Sprouts salad', 'Poha light'],
            'lunch': ['Dal chawal', 'Veg khichdi', 'Roti sabji dal', 'Veg soup rice', 'Palak paneer roti', 'Moong dal rice'],
            'dinner': ['Veg soup', 'Roti light curry', 'Salad bowl', 'Khichdi curd', 'Boiled veg rice'],
            'snacks': ['Apple', 'Orange', 'Roasted chana', 'Cucumber salad', 'Carrot sticks', 'Green tea']
        },
        'medium': {
            'breakfast': ['Poha with peanuts', 'Veg upma', 'Besan cheela', 'Stuffed paratha', 'Dosa sambar', 'Oats with fruits'],
            'lunch': ['Paneer bhurji roti', 'Rajma rice', 'Veg biryani', 'Dal makhani roti', 'Aloo gobhi rice', 'Chole roti'],
            'dinner': ['Veg pulao curd', 'Roti paneer', 'Stuffed roti', 'Veg stew', 'Palak rice'],
            'snacks': ['Mixed nuts', 'Fruit smoothie', 'Dhokla', 'Sprouts chat', 'Peanut butter toast']
        },
        'high': {
            'breakfast': ['Paneer paratha', 'Masala dosa', 'Stuffed poha', 'Aloo paratha', 'Veg sandwich heavy', 'Cheese toast'],
            'lunch': ['Paneer butter masala', 'Veg biryani full', 'Mixed veg rice', 'Stuffed paratha', 'Matar paneer roti', 'Veg fried rice'],
            'dinner': ['Veg thali', 'Paneer tikka masala', 'Rich veg curry', 'Naan with curry', 'Stuffed capsicum rice'],
            'snacks': ['Dry fruits', 'Milkshake', 'Cheese sandwich', 'Nut bar', 'Banana shake', 'Sweet lassi']
        }
    }

    nonveg_meals = {
        'low': {
            'breakfast': ['Boiled eggs (2)', 'Egg white omelette', 'Boiled egg salad', 'Egg bhurji light', 'Grilled chicken salad'],
            'lunch': ['Egg curry rice', 'Grilled fish salad', 'Chicken clear soup rice', 'Egg salad', 'Fish light curry'],
            'dinner': ['Chicken soup', 'Grilled fish', 'Egg whites', 'Light chicken curry'],
            'snacks': ['Boiled egg', 'Egg white', 'Chicken soup', 'Fish light']
        },
        'medium': {
            'breakfast': ['Egg omelette', 'Chicken keema paratha', 'Egg dosa', 'Fish sandwich', 'Chicken roll'],
            'lunch': ['Chicken curry rice', 'Egg masala roti', 'Fish fry rice', 'Chicken stew', 'Egg biryani'],
            'dinner': ['Grilled chicken', 'Fish curry roti', 'Chicken tikka', 'Egg curry'],
            'snacks': ['Chicken tikka', 'Fish fingers', 'Egg salad', 'Chicken drumstick']
        },
        'high': {
            'breakfast': ['Egg paratha', 'Chicken sandwich', 'Mutton keema', 'Fish cutlet', 'Chicken omelette'],
            'lunch': ['Chicken biryani', 'Mutton curry rice', 'Fish masala rice', 'Chicken steak', 'Egg fried rice'],
            'dinner': ['Butter chicken', 'Fish fry heavy', 'Mutton roast', 'Chicken korma', 'Rich egg curry'],
            'snacks': ['Chicken nuggets', 'Fish pakora', 'Mutton kebab', 'Egg masala', 'Protein shake chicken']
        }
    }
    
    # Select meals based on preference
    if preference == 'veg':
        food_set = veg_meals[level]
    else:
        food_set = nonveg_meals[level]
    
    # VARIATION 1: Random sample of 2 + choice
    breakfast = random.choice(food_set['breakfast']) 
    lunch = random.choice(food_set['lunch'])
    dinner = random.choice(food_set['dinner'])
    snacks_list = random.sample(food_set['snacks'], min(2, len(food_set['snacks'])))
    snacks = ' & '.join(snacks_list)
    
    # VARIATION 2: Goal modifiers
    if goal == 'weight_loss':
        dinner = 'Light ' + dinner.lower()
        snacks = snacks + ' (low cal)'
    elif goal == 'weight_gain':
        breakfast = breakfast + ' + extra nuts'
        dinner = dinner + ' + rice'
    
    # VARIATION 3: Activity modifiers
    if activity == 'high':
        lunch = lunch + ' + double portion'
    elif activity == 'low':
        dinner = 'Very light ' + dinner.lower()
    
    # VARIATION 4: Age-based modifier
    if age < 25:
        snacks += ' + energy drink'
    elif age > 50:
        breakfast = 'Healthy ' + breakfast
    
    return {
        'bmi': round(bmi, 1),
        'bmr': round(bmr, 0),
        'daily_calories': calories,
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snacks': snacks,
        'water_intake': f"{water // 1000}.{water % 1000 // 100} liters"
    }

def get_chat_response(message: str) -> str:
    msg = message.lower()
    random.seed(message)  # Deterministic but varied
    
    weight_loss_tips = [
        "For weight loss, create 500 cal deficit daily with veggies & protein.",
        "Cut sugar/carbs, eat high-fiber foods like oats & green veggies.",
        "Intermittent fasting + walking works great for fat loss.",
        "Avoid late night eating - finish dinner by 7 PM.",
        "Drink green tea & lemon water for metabolism boost."
    ]
    
    protein_tips = [
        "Best proteins: Eggs, chicken breast, fish, paneer, dal, greek yogurt.",
        "Aim 1.6-2.2g protein per kg bodyweight daily.",
        "Post-workout: Whey or chicken within 30 mins.",
        "Veg sources: Paneer (25g/100g), lentils (9g/100g cooked)."
    ]
    
    veg_tips = [
        "Veg power foods: Paneer, soya chunks, greek yogurt, quinoa, lentils.",
        "Combine dal + rice for complete protein.",
        "Sprouts + curd = high protein veg meal.",
        "Include all colors of veggies for micronutrients."
    ]
    
    water_tips = [
        "30-40ml per kg bodyweight (70kg = 2.1-2.8L daily).",
        "Drink 500ml 30 mins before meals for weight control.",
        "Add lemon/cucumber/mint for flavored water.",
        "First thing morning: 500ml warm water + lemon."
    ]
    
    exercise_tips = [
        "30 mins brisk walk daily burns 200+ calories.",
        "Strength training 3x/week preserves muscle during weight loss.",
        "HIIT 20 mins = 400 cal burn + afterburn effect."
    ]
    
    if any(word in msg for word in ['weight loss', 'lose weight', 'fat loss']):
        return random.choice(weight_loss_tips)
    elif any(word in msg for word in ['protein', 'muscle']):
        return random.choice(protein_tips)
    elif any(word in msg for word in ['veg', 'vegetarian']):
        return random.choice(veg_tips)
    elif 'water' in msg:
        return random.choice(water_tips)
    elif any(word in msg for word in ['exercise', 'workout', 'gym']):
        return random.choice(exercise_tips)
    else:
        general = [
            "Balance carbs/protein/fat 40/30/30 ratio.",
            "Sleep 7-8 hrs - poor sleep = hunger hormones.",
            "Track calories first 2 weeks to learn portions.",
            "Consistency > perfection in diet journey.",
            "Whole foods > supplements always."
        ]
        return random.choice(general)

