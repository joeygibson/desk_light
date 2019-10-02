class NumberGenerator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.val = min_value

    def __iter__(self):
        self.started = False

        return self

    def __next__(self):
        if not self.started:
            self.started = True
        else:
            tmp_val = self.val + 1

            if tmp_val > self.max_value:
                tmp_val = self.min_value

            self.val = tmp_val

        return self.val
