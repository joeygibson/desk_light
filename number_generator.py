class NumberGenerator:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.val = min
        self.direction = 'up'

    def __iter__(self):
        self.started = False

        return self

    def __next__(self):
        tmp_val = self.val

        if not self.started:
            self.started = True
        else:
            if self.direction == 'up':
                tmp_val = tmp_val + 1

                if tmp_val > self.max:
                    self.direction = 'down'
                    tmp_val = self.val - 1
            else:
                tmp_val = tmp_val - 1

                if tmp_val < self.min:
                    self.direction = 'up'
                    tmp_val = self.val + 1

            self.val = tmp_val

        return self.val