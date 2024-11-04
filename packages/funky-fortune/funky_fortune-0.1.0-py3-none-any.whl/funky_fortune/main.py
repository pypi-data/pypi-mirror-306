import random

def zodiac_fortune(sign):
    fortunes = {
        "Aries": ["You'll meet a talking sheep today", "Watch out for ram horns", "Your wool sweater will bring good luck"],
        "Taurus": ["Today is perfect for beef noodles", "You'll find a gold coin", "Don't be as stubborn as a bull"],
        "Gemini": ["Your other half is particularly annoying today", "Try writing with both hands simultaneously", "You're especially changeable today"],
        "Cancer": ["Don't hide in your shell", "Today is great for seafood", "Your pincers are extra strong today"],
        "Leo": ["Your roar will turn heads today", "Avoid big cats, they’re jealous", "A golden opportunity is coming your way"],
        "Virgo": ["Your attention to detail will be appreciated", "Clean up your room for a clearer mind", "Something green will bring you luck"],
        "Libra": ["Balance is key today", "You may find yourself attracted to shiny things", "Your charm will open doors"],
        "Scorpio": ["Secrets may come to light", "Channel your inner mystery", "Your sting can be powerful, use it wisely"],
        "Sagittarius": ["Adventure awaits you today", "Your aim is true, trust yourself", "You may have an urge to travel"],
        "Capricorn": ["Hard work pays off today", "Remember, even a mountain goat needs rest", "Your ambition will inspire others"],
        "Aquarius": ["Innovation is in your future", "Today is perfect for trying something new", "An unexpected friend will surprise you"],
        "Pisces": ["Your intuition is strong today", "Look for answers in your dreams", "Today is great for creative endeavors"]
    }
    return random.choice(fortunes.get(sign, ["Your zodiac sign is too special, I can't predict it"]))

def lucky_number(name):
    return sum(ord(char) for char in name) % 100

def fortune_cookie(lucky=False):
    fortunes = [
        "You'll be very lucky today",
        "Slow and steady wins the race",
        "Today is perfect for trying new things",
        "Remember to call your family"
    ]
    if lucky:
        return "Extra lucky: " + random.choice(fortunes)
    return random.choice(fortunes)

def magic_8ball(question):
    responses = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "You may rely on it",
        "My reply is no",
        "Better not tell you now",
        "Outlook not so good",
        "Cannot predict now"
    ]
    return f"Question: {question}\nAnswer: {random.choice(responses)}"

def main():
    while True:
        print("\n=== Mystic Fortune Teller ===")
        print("1. Zodiac Fortune")
        print("2. Lucky Number")
        print("3. Fortune Cookie")
        print("4. Magic 8 Ball")
        print("5. Exit")
        
        choice = input("\nChoose your option (1-5): ")
        
        if choice == "1":
            sign = input("Enter your zodiac sign (e.g., Aries): ")
            print("\nYour fortune is:", zodiac_fortune(sign))
            
        elif choice == "2":
            name = input("Enter your name: ")
            print("\nYour lucky number is:", lucky_number(name))
            
        elif choice == "3":
            want_lucky = input("Want extra luck? (yes/no): ").lower() == 'yes'
            print("\nYour fortune cookie says:", fortune_cookie(want_lucky))
            
        elif choice == "4":
            question = input("What's your question? ")
            print("\n", magic_8ball(question))
            
        elif choice == "5":
            print("Thank you for using Mystic Fortune Teller. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
