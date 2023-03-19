
#import database of many message, here is an example of 69
messages = [
    "Hey! How are you doing today?",
    "What are you up to?",
    "How was your day?",
    "How's the weather where you are?",
    "Did you watch that show I recommended?",
    "What have you been reading lately?",
    "Do you have any plans for the weekend?",
    "How's work/school going?",
    "What did you do over the weekend?",
    "What's new with you?",
    "Hey there, gorgeous. How's your day going?",
    "Hey there, handsome. How's your day going?",
    "I can't stop thinking about you.",
    "You looked amazing today.",
    "What are you wearing?",
    "I miss you so much.",
    "I can't wait to see you again.",
    "You make me so happy.",
    "Have you ever thought about us being more than friends?",
    "I love spending time with you.",
    "You're the best thing that's ever happened to me.",
    "I'm sorry for what I said/did.",
    "I didn't mean to hurt you.",
    "Please forgive me.",
    "I feel terrible about what happened.",
    "I understand if you're upset with me.",
    "I promise it won't happen again.",
    "I know I messed up.",
    "Can we talk about what happened?",
    "I want to make things right.",
    "Please don't be mad at me.",
    "I have a question...",
    "Just wanted to check in and see how you're doing.",
    "I'm so grateful for our friendship.",
    "Thanks for always being there for me.",
    "Want to hang out sometime this week?",
    "You're an amazing friend.",
    "I miss you, let's catch up soon.",
    "Can I vent to you for a minute?",
    "I appreciate your honesty.",
    "You're like a sibling to me.",
    "You make my life better just by being in it.",
    "How's your mum doing?",
    "How's your dad doing?",
    "How's your sister doing?",
    "How's your brother doing?",
    "Just wanted to say I love you.",
    "Thinking of you today.",
    "Have you spoken to grandma recently?",
    "Have you spoken to grandad recently?",
    "I'm proud of you.",
    "Thanks for everything you've done for me.",
    "Can't wait to see you at the party!",
    "Let's plan a family vacation soon.",
    "You're the best friend anyone could ask for.",
    "I'm grateful to have you in my life.",
    "What time are we meeting up?",
    "Where should we go for dinner tonight?",
    "Do you need a ride to the airport?",
    "I'll be there in ten minutes.",
    "What's the address of the party?",
    "Can you pick up some milk on your way home?",
    "Let's reschedule for next week.",
    "I have to cancel our plans, I'm sorry.",
    "What's your availability next week?",
    "Let's plan a trip together soon.",
    "Congrats on the new job!",
    "You did amazing on that presentation.",
    "You look great today.",
    "I'm so proud of you.",
    "You're so talented.",
    "Congrats on the engagement.",
    "Congrats on the marriage.",
    "Congrats on the baby.",
    "You're an inspiration to me.",
    "You're so kind.",
    "You're so thoughtful.",
    "You're so generous.",
    "I admire your strength.",
    "You make the world a better place."
    "What's your favorite movie/book/song?",
    "Do you have any pets?",
    "How many siblings do you have?",
    "What's your job?",
    "Where are you from?",
    "What's your favorite food?",
    "What's your favorite hobby?",
    "How old are you?",
    "What's your favorite color?",
    "What's your favorite season?",
    "Do you like sports?",
    "Are you a morning person or a night owl?",
    "Do you prefer tea or coffee?",
    "Do you have any allergies?",
    "What's your favorite TV show?",
    "Nice new hair cut, bro!",
    "Chem floor 6? Which room?",
    "Fancy getting a drink later ;)",
    "Want to grab a cup of coffee?",
    "Am running late",
    "I'm in the EEE bottom floor labs rn, want to cry"

]


switcher = {
    "A": 4,
    "B": 8,
    "C": 6,
    "D": 6,
    "E": 3,
    "F": 7,
    "G": 7,
    "H": 5,
    "I": 4,
    "J": 9,
    "K": 4,
    "L": 6,
    "M": 6,
    "N": 5,
    "O": 4,
    "P": 8,
    "Q": 9,
    "R": 5,
    "S": 5,
    "T": 3,
    "U": 6,
    "V": 8,
    "W": 7, 
    "X": 2,
    "Y": 7,
    "Z": 10
}

letter_counts = {}

for i in range(len(messages)):

    my_message = messages[i]
    

    #replaces spaces with x
    my_message=my_message.replace(' ', "x")

    #removes all special characters and numbers
    special_characters=['@','#','$','*','&','!','"','%',"'",'(',')','+',',','-','.','/','<',':',';','=','>','?', '[','\\',']','^','_','`','{','}','|','~','1','2','3','4','5','6','7','8','9','0']
    for j in special_characters:
        my_message = my_message.replace(j,"")
        
    #makes all letters upper case
    my_message=my_message.upper()

    #print(my_message)

    for letter in my_message:

        # Creates a dictionary to hold the letter counts for this message
        if letter in letter_counts:
            letter_counts[letter] += 1
        else:
            letter_counts[letter] = 1

    num_letters = len(my_message)
    #print(num_letters)

    taps_count = 0

    # Prints the letter counts for each letter
    for letter, count in letter_counts.items():
        taps_count += switcher[letter] * count
        #print(f"{letter}: {count}")
    #print("Tap count:", taps_count)
    print(taps_count)

    letter_counts = {}


    

