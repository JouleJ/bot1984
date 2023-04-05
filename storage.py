import pickle

# TODO: Use key-value database
class Storage:
    def __init__(self, initial_score=100.):
        self.initial_score = initial_score
        self.scores = dict()
        self.names = dict()

    def get_score(self, user_id):
        return self.scores.get(user_id, self.initial_score)

    def set_score(self, user_id, new_score):
        self.scores[user_id] = new_score

    def get_name(self, user_id):
        return self.names[user_id]

    def set_name(self, user_id, name):
        self.names[user_id] = name

    def list_everyone(self):
        result = []
        for user_id in self.scores:
            score = self.scores[user_id]
            result.append((user_id, score))
        return result

    def load_from(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                self = pickle.load(f)
        except:
            print('Failed to read from {}'.format(file_path))

    def save_to(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
