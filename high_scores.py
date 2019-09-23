import re


class HighScores:
    scores = []

    @staticmethod
    def natural_key(string_):
        return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

    def read_from_file(self, path):
        new_scores = []
        try:
            with open(path, "r") as f:
                for line in f:
                    new_scores.append(line.rstrip())
        except OSError as e:
            print("Unable to read high scores file!", e)

        new_scores.sort(key=HighScores.natural_key, reverse=True)
        self.scores = new_scores

    def get_scores(self):
        return self.scores

    def add_score(self, player_name, score):
        self.scores.append(str(score) + " " + player_name)
        self.scores.sort(key=HighScores.natural_key, reverse=True)

    def write_to_file(self, path):
        try:
            with open(path, "w") as f:
                for line in self.scores:
                    f.write(line + "\n")
        except OSError as e:
            print("Error writing high scores file!", e)
