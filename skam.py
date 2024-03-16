from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Sample dataset of text messages (replace with your own dataset)
text_messages = [
    ("Congratulations! You've won a free cruise. Claim now!", True),
    ("Your account has been compromised. Click here to verify your information.", True),
    ("Your package delivery failed. Click on the link to reschedule.", True),
    ("Get rich quick! Invest now and earn huge profits.", True),
    ("Urgent: Your bank account has been frozen. Please provide your credentials to unlock it.", True),
    ("Your computer is infected! Download our software to fix it.", True),
    ("Help us fight fraud! Provide your personal details for verification.", True),
    ("Your PayPal account has been suspended. Log in to resolve the issue.", True),
    ("Congratulations! You're our lucky winner. Claim your prize now.", True),
    ("Important notice: Your subscription is about to expire. Click here to renew.", True),
    ("Job opportunity: Work from home and earn $5000 per week.", True),
    ("Your social security number has been compromised. Call now to secure your identity.", True),
    ("Free iPhone giveaway! Just enter your details to participate.", True),
    ("Your email account has been hacked. Click here to reset your password.", True),
    ("IRS Tax Refund Alert! Click here to claim your refund.", True),
    ("Your bank has detected suspicious activity. Please log in to review your transactions.", True),
    ("Your Amazon account has been locked. Verify your information to unlock it.", True),
    ("Become a millionaire overnight! Join our investment program now.", True),
    ("Win a brand new car! Just fill out this survey to enter.", True),
    ("Your credit card has been charged for unauthorized transactions. Call now to dispute.", True),
    ("Congratulations! You've been selected for a special offer. Redeem now.", True),
    ("Your Facebook account has been reported. Click here to verify your identity.", True),
    ("Help us test our new product and get a free trial. Limited time offer!", True),
    ("Your Netflix subscription has expired. Click here to update your payment information.", True),
    ("Your phone number has been selected as a winner. Claim your prize now!", True),
    ("Important security alert: Your account has been locked. Click here to unlock.", True),
    ("Your Google account has been compromised. Log in to secure it.", True),
    ("Special discount: 50% off on all purchases. Click here to shop now!", True),
    ("Your online banking session has expired. Log in again to continue.", True),
    ("Claim your inheritance! Provide your bank details to receive the funds.", True),
    ("Your email has won a prize. Reply with your details to claim.", True),
    ("$10 Nitro Gift! You’ve been gifted a 1 Month Nitro Games https://discord.birth/kjqsSQDF4qs9f4sK456ds7 152 Click on the link to accept & add the bot Hello for our anniversary we decided to gift to all Discord users!", True),
    ("YOU’VE WON A NITRO EVENT! Hey, you have won a $10 Discord Nitro event in Nitro Haven | Social . Anime . E-Girls (Discord) however you have left the server. please rejoin and message Caitt#6783 to claim your prize", True),
    ("You won 5000 Robux! To accept, all you have to do is press the link below, invite the bot to all servers you own, then the gift cards will appear", True),
    ("Bro i made a game can you test play? tell me if something is wrong in the game thanks :3 https://github.com/bxrg3mxn/bxrg3mxn/blob/main/M5Game_v3.rar", True),
    ("• Get Discord Nitro for Free from Steam Store • Free 3 months Discord Nitro • The offer is valid until at 6: 00PM on November 31, 2021. Personalize your profile, screen share in HD, upgrade your emojis, and more. Click to get Nitro: https://startfullds.com/", True),
    ("BEST NSFW", True),
    ("Hurry! Only a few spots left in free NITRO", True),
    ("Free skins!!! Give me a trade link", True),
    ("Get a chance to win a brand new iPhone! Just click on the link to participate in our giveaway.", True),
    ("Congratulations! You've been selected as the winner of our weekly prize draw. Claim your reward now by clicking the link.", True),
    ("Limited time offer: Free Netflix subscription for 6 months. Click here to claim your reward.", True),
    ("You've received a message from your bank regarding suspicious activity on your account. Click the link to verify your identity.", True),
    ("Reminder: Your discord nitro is expiring soon. Renew now to continue enjoying our services.", True),
    ("Free nitro :333 Just click that link ", True),
    ("Click the link, get the prise :)", True),
    ("Hey, how are you? Let's catch up sometime.", False),
    ("Hello there, How are you guys?", False),
    ("Thanks for joining our discussion about the latest game patch. What do you think about the new changes?", False),
    ("Need help with a quest in Skyrim. Can anyone give me tips on how to complete it?", False),
    ("Good morning! Have a great day ahead.", False),
    ("Here's the link to the Google Drive folder with the meeting agenda.", False),
    ("Hey, can someone help me troubleshoot this coding problem?", False),
    ("Welcome back! We missed your ass yesterday's game session :c", False),
    ("Hello! How was your day? Let's plan a meetup soon.", False),
    ("I'm organizing a charity event next week. Would you like to volunteer?", False),
    ("Thank you for your purchase! Your order has been successfully processed.", False),
    ("Looking forward to seeing you at the party tomorrow night!", False),
    ("Don't forget to submit your assignment by the end of the week.", False),
    ("Here's the link to the document you requested. Let me know if you need any further assistance.", False),
    ("Congratulations on your promotion! Let's celebrate over dinner tonight.", False),
    ("Reminder: The meeting has been rescheduled to 3 PM. Please adjust your calendar accordingly.", False),
    ("Good luck on your exam tomorrow! You've got this.", False),
    ("Hey, how are you? Let's catch up sometime.", False),
    ("Hello there, How are you guys?", False),
    ("Thanks for joining our discussion about the latest game patch. What do you think about the new changes?", False),
    ("Need help with a quest in Skyrim. Can anyone give me tips on how to complete it?", False),
    ("Good morning! Have a great day ahead.", False),
    ("Here's the link to the Google Drive folder with the meeting agenda.", False),
    ("Hey, can someone help me troubleshoot this coding problem?", False),
    ("Welcome back! We missed your ass yesterday's game session :c", False),
    ("Hello! How was your day? Let's plan a meetup soon.", False),
    ("I'm organizing a charity event next week. Would you like to volunteer?", False),
    ("Thank you for your purchase! Your order has been successfully processed.", False),
    ("Looking forward to seeing you at the party tomorrow night!", False),
    ("Don't forget to submit your assignment by the end of the week.", False),
    ("Here's the link to the document you requested. Let me know if you need any further assistance.", False),
    ("Congratulations on your promotion! Let's celebrate over dinner tonight.", False),
    ("Reminder: The meeting has been rescheduled to 3 PM. Please adjust your calendar accordingly.", False),
    ("Good luck on your exam tomorrow! You've got this.", False),
    ("Hey, how are you? Let's catch up sometime.", False),
    ("Hello there, How are you guys?", False),
    ("Thanks for joining our discussion about the latest game patch. What do you think about the new changes?", False),
    ("Need help with a quest in Skyrim. Can anyone give me tips on how to complete it?", False),
    ("Good morning! Have a great day ahead.", False),
    ("Here's the link to the Google Drive folder with the meeting agenda.", False),
    ("Hey, can someone help me troubleshoot this coding problem?", False),
    ("Welcome back! We missed your ass yesterday's game session :c", False),
    ("Hello! How was your day? Let's plan a meetup soon.", False),
    ("I'm organizing a charity event next week. Would you like to volunteer?", False),
    ("Thank you for your purchase! Your order has been successfully processed.", False),
    ("Looking forward to seeing you at the party tomorrow night!", False),
    ("Don't forget to submit your assignment by the end of the week.", False),
    ("Here's the link to the document you requested. Let me know if you need any further assistance.", False),
    ("Congratulations on your promotion! Let's celebrate over dinner tonight.", False),
    ("Reminder: The meeting has been rescheduled to 3 PM. Please adjust your calendar accordingly.", False),
    ("Good luck on your exam tomorrow! You've got this.", False),
    ("Have a great weekend!", False)
]

# Separate text and labels
texts, labels = zip(*text_messages)

# Vectorize the text using bag-of-words representation
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.5, random_state=44)

# Train Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = classifier.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)

def check(txt):
    # Example usage: Predict if a new text message is a scam or not
    new_text = []
    new_text.append(txt)

    new_text_vectorized = vectorizer.transform(new_text)
    prediction = classifier.predict(new_text_vectorized)
    return prediction[0]

check('Click the link, get the prise :)')