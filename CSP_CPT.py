## AP CSP:- Credit Score Simulation

# List manages the storage of credit score ranges and where the user's score fits.
# Each dictionary represents a "Level" of credit score health.
loan_tiers = [
    {"min_score": 300, "max_score": 579, "base_rate": 18.5, "label": "Poor"},
    {"min_score": 580, "max_score": 669, "base_rate": 14.5, "label": "Fair"},
    {"min_score": 670, "max_score": 739, "base_rate": 10.5, "label": "Good"},
    {"min_score": 740, "max_score": 799, "base_rate": 6.5, "label": "Very Good"},
    {"min_score": 800, "max_score": 850, "base_rate": 3.5, "label": "Exceptional"},
]

# Algorithm which simulates credit score calculation based on various factors.
def calculate_interest(credit_score, amount):
    final_rate = 0
    tier_name = ""

    #Iteration:- Loop looks thru the list of baank rules.
    for tier in loan_tiers:
        # Find the correct range for the user's score.
        if credit_score >= tier["min_score"] and credit_score <= tier["max_score"]:
            final_rate = tier["base_rate"]
            tier_name = tier["label"]

            # Further logic based on requested loan amount.
            # If user asks for more than $50K, bank adds "risk interest" to the base_rate defined in the dictionary.
            if amount > 50000:
                final_rate += 2.5 # Risk interest for large loans

    return tier_name, final_rate

# Generate a random credit score for the user using imported "random" module.
user_score = 0
time_period = 0.0
user_request = 0.0

while user_score < 300 or user_score > 850:
    user_score = int(input("Please enter your credit score (300-850): "))
    if user_score < 300 or user_score > 850:
        print("Invalid credit score. Score must be between 300 and 850.")

while type(user_request) != float or user_request <= 0:
    user_request = float(input("Enter the loan amount you wish to apply for: "))
    if type(user_request) != float or user_request <= 0:
        print("Invalid loan amount. Please enter a positive number.")

while type(time_period) != float or time_period <= 0:
    time_period = float(input("Enter the loan term in years (only numbers): "))
    if type(time_period) != float or time_period <= 0:
        print("Invalid loan term. Please enter a positive number.")

category, rate = calculate_interest(user_score, user_request)

# Use the compound interest formula (A = P(1 + r/n)^(nt)) to calculate the total amount owed to the bank after the loan term.
print(f"-" * 100)
print(f"Your credit score is: {user_score} ({category})")
if user_request > 50000:
    print(f"Due to the high loan amount, an additional risk interest has been added to your base rate.")
print(f"Predicted interest rate for your loan based on given metrics: {rate}%")
print(f"-" * 100)
print(f"Estimated total value of your loan after {time_period} years (compounding annually): ${user_request * (1 + (rate/100)) ** time_period:.2f}")
print(f"-" * 100)
