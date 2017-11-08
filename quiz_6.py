# Creates a class to represent a permutation of 1, 2, ..., n for some n >= 0.
#
# An object is created by passing as argument to the class name:
# - either no argument, in which case the empty permutation is created, or
# - "length = n" for some n >= 0, in which case the identity over 1, ..., n is created, or
# - the numbers 1, 2, ..., n for some n >= 0, in some order, possibly together with "lengh = n".
#
# __len__(), __repr__() and __str__() are implemented, the latter providing the standard form
# decomposition of the permutation into cycles (see wikepedia page on permutations for details).
#
# Objects have:
# - nb_of_cycles as an attribute
# - inverse() as a method
#
# The * operator is implemented for permutation composition, for both infix and in-place uses.
#
# Written by Daniel Yang and Eric Martin for COMP9021


class PermutationError(Exception):
    def __init__(self, message):
        self.message = message

class Permutation:
    def __init__(self, *args, length = None):
        if not all(isinstance(e, int) for e in args):
            raise PermutationError("Cannot generate permutation from these arguments")
        if args and length:
            if len(args) != length or set(args) != set(range(1, length + 1)):
                raise PermutationError("Cannot generate permutation from these arguments")
            else:
                self.perm = args
        elif not args and length:
            if length < 0:
                raise PermutationError("Cannot generate permutation from these arguments")
            self.perm = tuple(range(1, length + 1))
        elif args and not length:
            if set(args) != set(range(1, len(args) + 1)):
                raise PermutationError("Cannot generate permutation from these arguments")
            else:
                self.perm = args
        else:
            self.perm = args
        self._decompose_cycles()
        
    def __len__(self):
        return len(self.perm)

    def __repr__(self):
        return f"Permutation{self.perm}"

    def __str__(self):
        outputString = ""
        for cycle in self.cycles:
            outputString += "(" + " ".join(str(e) for e in cycle) + ")"
        if not outputString:
            outputString = "()"
        return outputString

    def __mul__(self, permutation):
        if len(self) != len(permutation):
            raise PermutationError("Cannot compose permutations of different lengths")
        return Permutation(*(permutation.perm[e - 1] for e in self.perm))

    def __imul__(self, permutation):
        if len(self) != len(permutation):
            raise PermutationError("Cannot compose permutations of different lengths")
        return Permutation(*(permutation.perm[e - 1] for e in self.perm))

    def inverse(self):
        return Permutation(*(self.perm.index(i + 1) + 1 for i in range(len(self.perm))))

    def _decompose_cycles(self):
        done = []
        cycles = []
        
        for i in range(len(self.perm)):
            if i not in done:
                done.append(i)
                cycle = [i + 1]
                while True:
                    j = self.perm[cycle[-1] - 1]
                    if j not in cycle:
                        cycle.append(j)
                        done.append(j - 1)
                    else:
                        break
                cycles.append(tuple(cycle[cycle.index(max(cycle)):] + cycle[:cycle.index(max(cycle))]))
        self.cycles = sorted(cycles)
        self.nb_of_cycles = len(self.cycles)