class switch:
    def __init__(self, *caseOutPairs, end=None):
        self.dictionary = {}
        # Check for odd caseOutPairs length and set the last as end if needed
        if len(caseOutPairs) % 2 != 0:
            self.end = caseOutPairs[-1]
            caseOutPairs = caseOutPairs[:-1]  # Remove last item from cases
        else:
            self.end = end  # Use specified end if provided

        # Populate the dictionary with case-output pairs
        for i in range(0, len(caseOutPairs), 2):
            case = caseOutPairs[i]
            output = caseOutPairs[i+1]
            self.dictionary[case] = output

    def __call__(self, matchCase, *args, **kwargs):
        if matchCase in self.dictionary:
            result = self.dictionary[matchCase]
            if callable(result):
                return result(*args, **kwargs)  # Pass arguments if callable
            else:
                return result
        else:
            if callable(self.end):
                return self.end(*args, **kwargs)  # Pass arguments if callable
            else:
                return self.end

    def __getitem__(self, case, *args, **kwargs):
        if case in self.dictionary:
            result = self.dictionary[case]
            if callable(result):
                return lambda *args, **kwargs: result(*args, **kwargs)
            else:
                return result
        else:
            if callable(self.end):
                return lambda *args, **kwargs: self.end(*args, **kwargs)
            else:
                return self.end

    def __setitem__(self, case, result):
        self.dictionary[case] = result

    def __repr__(self):
        endString = ""
        for k in self.dictionary.keys():
            endString += f"{k}:{self(k)}\n"
        return endString

    def __str__(self):
        return self.__repr__()
