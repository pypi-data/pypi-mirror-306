class ArgumentChecker:
    def __init__(self):
        self.errors = []

    def is_true(self, condition, *message_parts):
        if not condition:
            message = " ".join(map(str, message_parts)) or "Argument is ill defined."
            self.errors.append(message)
            return False
        return True

    def has_length(self, arg, length, msg=None):
        if msg is None:
            msg = f"Argument does not have the required length of {length}."
        return self.is_true(len(arg) == length, msg)

    def not_condition(self, condition, *message_parts):
        return self.is_true(not condition, *message_parts)

    def one_of(self, arg, *options):
        options_str = ", ".join(f"'{opt}'" for opt in options)
        if len(options) == 2:
            options_str = " or ".join(options_str.split(", "))
        elif len(options) > 2:
            options_str = f"one of {options_str}"
        return self.is_true(arg in options, f"Argument is not {options_str}.")

    def within(self, arg, lower, upper):
        return self.is_true(lower <= arg <= upper, f"Argument is not within {lower} and {upper} (is {arg}).")

    def at_least(self, arg, lower, msg=None):
        if msg is None:
            msg = f"Argument is not greater or equal to {lower} (is {arg})."
        return self.is_true(arg >= lower, msg)

    def at_most(self, arg, upper, msg=None):
        if msg is None:
            msg = f"Argument is not less or equal to {upper} (is {arg})."
        return self.is_true(arg <= upper, msg)

    def by_class(self, param, class_name):
        return self.is_true(isinstance(param, class_name), f"Argument is not of class {class_name}.")

    def is_logical(self, param):
        return self.is_true(isinstance(param, bool), "Argument is not logical (boolean).")

    def check(self, *expressions):
        for i, expression in enumerate(expressions):
            if not expression:
                self.errors.append(f"Argument {i+1} is ill defined.")
        if self.errors:
            raise ValueError("\n".join(self.errors))