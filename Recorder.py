import csv


class RecordedGame:
    def __init__(self) -> None:
        self.recordedGameArray = []

    def recordGamestate(self, array):
        self.recordedGameArray.append(array)

    def snapGamestateEnd(self, seed, array, turn, player, folder):
        stringpath = "{0}{1}{2}{3}{4}{5}{6}".format(folder, seed, "|t_", turn, "|p_", player, ".csv")
        file = open(stringpath, 'w+', newline ='')
        with file:
            write = csv.writer(file)
            write.writerows(array)

    def snapGamestateEveryturn(self, seed, array, turn, score1, score2, folder):
        stringpath = "{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(folder, seed, "|t_", turn, "|p1_", score1, "|p2_", score2, ".csv")
        file = open(stringpath, 'w+', newline ='')
        with file:
            write = csv.writer(file)
            write.writerows(array)

    def snapGamestateWscores(self, seed, array, turn, player, score1, score2):
        stringpath = "{0}{1}{2}{3}{4}{5}{6}".format("/home/maciej/Desktop/Guesser/data/", seed, "t", turn, "p", player, ".csv")
        file = open(stringpath, 'w+', newline ='')
        with file:
            write = csv.writer(file)
            write.writerows(array)
            write.writerow([score1])
            write.writerow([score2])