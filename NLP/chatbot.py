

from nltk.chat.util import Chat, reflections


# ============================================================
# CHATBOT PATTERNS AND RESPONSES
# ============================================================

pairs = [

    [
        r"(.*)my name is (.*)",
        ["Hello %2, How are you today?"]
    ],

    [
        r"(.*)help(.*)",
        ["I can help you."]
    ],

    [
        r"(.*)your name ?",
        ["My name is the Clever Programmer, but you can just call me Robot. I'm a chatbot."]
    ],

    [
        r"how are you (.*) ?",
        ["I'm doing very well.", "I am great!"]
    ],

    [
        r"sorry (.*)",
        ["It's alright.", "It's OK, never mind that."]
    ],

    [
        r"i'm (.*) (good|well|okay|ok)",
        ["Nice to hear that.", "Alright, great!"]
    ],

    [
        r"(hi|hey|hello|hola|holla)(.*)",
        ["Hello!", "Hey there!"]
    ],

    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse."]
    ],

    [
        r"(.*)created(.*)",
        ["Prakash created me using Python's NLTK library.", "Top secret ;)"]
    ],

    [
        r"(.*) (location|city) ?",
        ["Hyderabad, India"]
    ],

    [
        r"(.*)raining in (.*)",
        [
            "No rain in the past 4 days here in %2.",
            "In %2 there is a 50% chance of rain."
        ]
    ],

    [
        r"how (.*) health (.*)",
        [
            "Health is very important, but I am a computer, "
            "so I don't need to worry about my health."
        ]
    ],

    [
        r"(.*)(sports|game|sport)(.*)",
        ["I'm a very big fan of Cricket."]
    ],

    [
        r"who (.*) (Cricketer|Batsman)?",
        ["Virat Kohli"]
    ],

    [
        r"quit",
        [
            "Bye for now. See you soon :)",
            "It was nice talking to you. See you soon :)"
        ]
    ],

    [
        r"(.*)",
        ["Our customer service will reach you."]
    ],
]


# ============================================================
# CHATBOT FUNCTION
# ============================================================

def chatbot():

    print("=" * 60)
    print("Hi, I am The Clever Programmer 🤖")
    print("I am an NLTK Chatbot.")
    print("Type 'quit' to exit.")
    print("=" * 60)

    # Create chatbot
    chat = Chat(pairs, reflections)

    # Start conversation
    chat.converse()


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":
    chatbot()
