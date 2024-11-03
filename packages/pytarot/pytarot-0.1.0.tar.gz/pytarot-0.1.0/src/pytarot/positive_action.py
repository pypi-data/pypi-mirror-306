import random

def get_positive_action():
    messages = [
        "Every step you take counts, no matter how small.",
        "Today is a new beginning, seize the opportunity.",
        "Keep smiling and trust that good things are coming your way.",
        "Challenges make you stronger, embrace each one.",
        "You are stronger than you think.",
        "Success is the sum of small efforts repeated day in and day out.",
        "Believe in yourself; you are capable of more than you know.",
        "Positive thoughts lead to positive outcomes.",
        "The best time for new beginnings is now.",
        "Your potential is endless, keep pushing forward."
    ]

    suggestions = [
        "Take five minutes to practice deep breathing for calm and focus.",
        "Write down three small goals for today and accomplish them one by one.",
        "Reach out to a friend or loved one and share something uplifting.",
        "Read a page of a book that inspires you.",
        "Write down one thing you're grateful for and savor that feeling.",
        "Take a short walk outside and appreciate the nature around you.",
        "Spend a few minutes stretching to release tension.",
        "Listen to your favorite motivational song.",
        "Drink a glass of water and stay hydrated.",
        "Organize a small part of your workspace for a fresh start.",
        "Try a 10-minute meditation session to clear your mind.",
        "Doodle or draw something to engage your creative side.",
        "Watch a short, funny video to boost your mood.",
        "Take a moment to list your accomplishments this week.",
        "Plan a small reward for completing a task today.",
        "Try cooking or baking something new and simple.",
        "Spend a few moments journaling your thoughts and ideas.",
        "Do a short bodyweight workout or yoga flow.",
        "Start a new hobby or revisit an old one for fun.",
        "Listen to a podcast or an audiobook that interests you."
    ]

    message = random.choice(messages)
    suggestion = random.choice(suggestions)

    output = f"Today's Positive Message: '{message}' Suggestion: {suggestion}"
    return output