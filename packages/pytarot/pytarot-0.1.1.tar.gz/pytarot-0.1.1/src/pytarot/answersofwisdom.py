import random

def get_answers_of_wisdom():
    wisdom_list = [
        "Patience is a virtue. Good things come to those who wait.",
        "The journey of a thousand miles begins with a single step.",
        "Believe in yourself, and the universe will align to support you.",
        "Sometimes, the best decision is no decision at all.",
        "Don’t count the days, make the days count.",
        "Let go of what you can’t change and focus on what you can control.",
        "Trust the timing of your life.",
        "Happiness is a choice, not a result.",
        "If you want to go fast, go alone. If you want to go far, go together.",
        "Embrace the uncertainty; sometimes the best stories come from the unexpected.",
        "Life is about learning from every experience, good or bad.",
        "Take life one day at a time and live in the moment.",
        "Your vibe attracts your tribe; be mindful of your energy.",
        "Opportunities don’t happen, you create them.",
        "Success is not the key to happiness. Happiness is the key to success."
        "You don’t need to have it all figured out to move forward.",
        "Growth comes when you step outside your comfort zone.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "Every day may not be good, but there’s something good in every day.",
        "What lies behind us and what lies before us are tiny matters compared to what lies within us.",
        "Dream big, start small, and act now.",
        "Failure is simply the opportunity to begin again, this time more intelligently.",
        "Courage is not the absence of fear, but the triumph over it."
    ]
    
    # Choose a random piece of wisdom from the list
    answer = random.choice(wisdom_list)
    
    return answer