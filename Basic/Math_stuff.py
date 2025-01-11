from mpmath import mp
class Pi_number:
    def __init__(self,numbers):
        self.numbers = numbers

    def calculate_pi(self):
        mp.dps = self.numbers
        pi_value = mp.pi
        return pi_value


numbers = int(input("How many digits of Pi to display?:"))

pi1 = Pi_number(numbers)
answers = pi1.calculate_pi()
print(f"Pi to the {numbers} digits is {answers}")

