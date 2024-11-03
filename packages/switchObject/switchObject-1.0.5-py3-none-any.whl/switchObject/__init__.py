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
            output = caseOutPairs[i + 1]
            self.dictionary[case] = output

    def __call__(self, matchCase, *args, **kwargs):
        if matchCase in self.dictionary:
            result = self.dictionary[matchCase]
            # If result is a switch, recursively call it
            if isinstance(result, switch):
                return result(matchCase, *args, **kwargs)
            elif callable(result):
                return result(*args, **kwargs)  # Pass arguments if callable
            else:
                return result
        else:
            # If end is a switch, recursively call it
            if isinstance(self.end, switch):
                return self.end(matchCase, *args, **kwargs)
            elif callable(self.end):
                return self.end(*args, **kwargs)  # Pass arguments if callable
            else:
                return self.end

    def __getitem__(self, case):
        result = self.dictionary.get(case, self.end)
        # Return a callable if result is callable or is a nested switch
        if callable(result) or isinstance(result, switch):
            return lambda *args, **kwargs: result(*args, **kwargs) if callable(result) else result
        else:
            return result

    def __setitem__(self, case, result):
        self.dictionary[case] = result

    def __repr__(self):
        items = []
        for k, v in self.dictionary.items():
            if isinstance(v, switch):
                # Indent nested switch instances
                nested_repr = repr(v).replace("\n", "\n\t")
                items.append(f"{k}:\n\t{nested_repr}")
            else:
                items.append(f"{k}: {repr(v)}")

        # Format the end case with indentation if it's a nested switch
        if self.end is not None:
            if isinstance(self.end, switch):
                end_repr = repr(self.end).replace("\n", "\n\t")
                items.append(f"default:\n\t{end_repr}")
            else:
                items.append(f"default: {repr(self.end)}")

        return "\n".join(items)

    def __str__(self):
        return self.__repr__()
