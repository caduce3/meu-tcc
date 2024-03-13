happy = 50
neutral = 36
surprise = 2
sad = 0
angry = 0
fear = 0
disgust = 0

def calcularPorcentagem(happy, neutral, surprise, sad, angry, fear, disgust):
    total = happy + neutral + surprise + sad + angry + fear + disgust
    happy_percent = (happy * 100) / total
    neutral_percent = (neutral * 100) / total
    surprise_percent = (surprise * 100) / total
    sad_percent = (sad * 100) / total
    angry_percent = (angry * 100) / total
    fear_percent = (fear * 100) / total
    disgust_percent = (disgust * 100) / total

    print(f"Happy: {happy_percent:.2f}%")
    print(f"Neutral: {neutral_percent:.2f}%")
    print(f"Surprise: {surprise_percent:.2f}%")
    print(f"Sad: {sad_percent:.2f}%")
    print(f"Angry: {angry_percent:.2f}%")
    print(f"Fear: {fear_percent:.2f}%")
    print(f"Disgust: {disgust_percent:.2f}%")

calcularPorcentagem(happy, neutral, surprise, sad, angry, fear, disgust)
