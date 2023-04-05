from transformers import pipeline

model = pipeline('sentiment-analysis', model='s-nlp/russian_toxicity_classifier')

def evaluate(text):
    result = model(text)

    assert len(result) == 1
    result = result[0]

    if result['label'] == 'neutral':
        return result['score']
    elif result['label'] == 'toxic':
        return -result['score']
    else:
        return None


def compute_updated_user_score(old_user_score, message_score):
    if message_score < 0:
        return old_user_score * (1. + 0.05 * message_score)
    else:
        return old_user_score + message_score
