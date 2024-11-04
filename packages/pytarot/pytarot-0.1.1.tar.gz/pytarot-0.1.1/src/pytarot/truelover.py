import random

def get_true_lover():
    job = ["Teacher", "Engineer", "Doctor", "Nurse", "Architect", "Software Developer", "Graphic Designer", "Chef", "Pilot", 
           "Lawyer", "Accountant", "Scientist", "Electrician", "Carpenter", "Mechanic", "Writer", "Artist", "Photographer", 
           "Pharmacist", "Veterinarian", "Social Worker", "Police Officer", "Firefighter", "Librarian", "Journalist", 
           "Marketing Specialist", "Salesperson", "Plumber", "Psychologist", "Data Analyst", "Financial Advisor", "Dentist", 
           "Actor", "Musician", "Farmer", "Translator", "Consultant", "Project Manager", "Researcher", "Chef", "Event Planner", 
           "Web Developer", "Therapist", "Fitness Trainer", "Fashion Designer", "Interior Designer", "Animator", "Biologist", 
           "Chemist", "Historian"]
    height = ["Very Short", "Short", "Below Average", "Average", "Above Average", "Tall", "Very Tall", "Extremely Tall"]
    eye_color = ["Brown", "Blue", "Green", "Hazel", "Amber", "Gray", "Violet", "Black", "Red"]
    hair_color = ["Black", "Brown", "Blonde", "Red", "Auburn", "Chestnut", "Gray", "White", "Silver", "Platinum Blonde", 
                  "Strawberry Blonde", "Blue", "Green", "Pink", "Purple", "Teal"]
    residence = ["House", "Apartment", "Condo", "Villa", "Cabin", "Cottage", "Mansion", "Farmhouse", "Bungalow", "Duplex", 
                 "Studio", "Loft", "Townhouse", "Mobile Home", "Penthouse", "Dormitory", "Hostel", "Boarding House", "Tiny House", 
                 "Yurt", "Chalet", "Tent", "RV", "Boat", "Caravan", "Castle", "Ranch", "Hut", "Treehouse", "Igloo", "Palace"]

    profile = {
        "Job": random.choice(job),
        "Height": random.choice(height),
        "Eye Color": random.choice(eye_color),
        "Hair Color": random.choice(hair_color),
        "Residence": random.choice(residence)
    }

    summary = f"A {profile['Job']}, who is {profile['Height']}, with {profile['Eye Color']} eyes, {profile['Hair Color']} hair, and lives in a {profile['Residence']}."

    
    return summary



    