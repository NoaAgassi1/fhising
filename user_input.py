# user_input.py
# Meir Shuker 318901527 Noa Agassi 209280635

def get_user_details():
    """
    Prompt the user for their details, using short codes and simple inputs:
     - Gender: M/F
     - Age: integer
     - Marital status: S = single, M = married
     - Number of kids: integer (0 = no kids)
     - Profession: free text (default "Unknown")
     - Full name: free text
    Returns a dict with full (expanded) values.
    """
    def prompt_choice(prompt, choices_map):
        while True:
            resp = input(f"{prompt} ({'/'.join(choices_map.keys())}): ").strip().upper()
            if resp in choices_map:
                return choices_map[resp]
            print(f"❌ Invalid choice. Please enter one of {', '.join(choices_map.keys())}.")

    def prompt_int(prompt):
        while True:
            resp = input(f"{prompt}: ").strip()
            if resp.isdigit():
                return int(resp)
            print("❌ Please enter a non-negative integer.")

    # 1. Gender
    gender = prompt_choice("Gender", {"M": "Male", "F": "Female"})

    # 2. Age
    age = prompt_int("Age")

    # 3. Marital status
    marital_status = prompt_choice("Marital status", {"S": "Single", "M": "Married"})

    # 4. Number of kids
    kids_count = prompt_int("Number of kids")

    # 5. Profession
    profession = input("Profession: ").strip() or "Unknown"

    # 6. Full name
    full_name = input("Full name: ").strip()

    return {
        "gender": gender,
        "age": age,
        "marital_status": marital_status,
        "kids": kids_count,
        "profession": profession,
        "full_name": full_name,
    }
