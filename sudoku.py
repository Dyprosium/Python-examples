from collections import defaultdict
from itertools import combinations

class Sudoku:
    def __init__(self, filename):
        grid, rows, columns, boxes, box_dict = [], [], [], [], defaultdict(list)
        with open(filename) as input:
            for line in input:
                try:
                    if line.strip():
                        grid.append([int(e) for e in line.strip().replace(" ", "")])
                except ValueError:
                    raise SudokuError("Incorrect input")
        for row in grid:
            r = Group(row)
            for cell in r.cells:
                cell.groups["row"] = r
            rows.append(r)
        for j in range(9):         
            c = Group([rows[i].cells[j] for i in range(len(rows))])
            for cell in c.cells:
                cell.groups["col"] = c
            columns.append(c)
        for i in range(9):
            for j in range(9):
                if 0 <= i <= 2:
                    if 0 <= j <= 2: 
                        box_dict[0].append(rows[i].cells[j])
                    if 3 <= j <= 5:
                        box_dict[1].append(rows[i].cells[j])
                    if 6 <= j <= 8:
                        box_dict[2].append(rows[i].cells[j])
                if 3 <= i <= 5:
                    if 0 <= j <= 2: 
                        box_dict[3].append(rows[i].cells[j])
                    if 3 <= j <= 5:
                        box_dict[4].append(rows[i].cells[j])
                    if 6 <= j <= 8:
                        box_dict[5].append(rows[i].cells[j])
                if 6 <= i <= 8:
                    if 0 <= j <= 2: 
                        box_dict[6].append(rows[i].cells[j])
                    if 3 <= j <= 5:
                        box_dict[7].append(rows[i].cells[j])
                    if 6 <= j <= 8:
                        box_dict[8].append(rows[i].cells[j])
        for i in range(9):
            b = Group(box_dict[i])
            for cell in b.cells:
                cell.groups["box"] = b
            boxes.append(b)
        self.rows, self.columns, self.boxes = tuple(rows), tuple(columns), tuple(boxes)
        self.filename = filename[ :-4]
        
        for row in self.rows:
            for cell in row.cells:
                cell.neighbours = {other for other in cell.groups["row"].cells + cell.groups["col"].cells + cell.groups["box"].cells if other != cell}
       
    def preassess(self):
        for group in self.rows + self.columns + self.boxes:
            nums = [cell.value for cell in group.cells if cell.value]
            if len(nums) != len(set(nums)):
                print("There is clearly no solution.")
                return
        print("There might be a solution.")
    
    def _force_digits(self):
        progress = True
        while progress:
            progress = False
            for box in self.boxes:
                missing = set(range(1,10)) - {cell.value for cell in box.cells if cell.value}
                for number in missing:
                    possible_cells = []
                    for cell in box.cells:
                        if cell.value or number in {other.value for other in cell.neighbours if other.value}:
                            continue
                        possible_cells.append(cell)
                    if len(possible_cells) == 1:
                        possible_cells[0].value = number
                        progress = True
    
    def _mark_cells(self):
        for row in self.rows:
            for cell in row.cells:
                if not cell.value:
                    cell.possible = set(range(1,10)) - {neighbour.value for neighbour in cell.neighbours if neighbour.value}
        
    def _solve(self):
        new_preset = True
        while new_preset:
            new_preset = False
            
            # check for any cells with only one possibility or any singletons
            new_insert = True
            while new_insert:
                new_insert = False
                for row in self.rows:
                    for cell in row.cells:
                        if len(cell.possible) == 1:
                            cell._update(list(cell.possible)[0])
                            new_insert = True
                for group in self.rows + self.columns + self.boxes:
                    for num in range(1,10):
                        possible_cells = []
                        for cell in group.cells:
                            if num in cell.possible:
                                possible_cells.append(cell)
                        if len(possible_cells) == 1:
                            possible_cells[0]._update(num)
                            new_insert = True
                            
            #try to find a new preset
            for group in self.rows + self.columns + self.boxes:
                empty_cells = [cell for cell in group.cells if not cell.value]
                for size in range(2, len(empty_cells)):
                    for comb in combinations(empty_cells, size):
                        u = set.union(*(cell.possible for cell in comb))
                        if comb not in group.presets and len(u) == size:
                            group.presets[comb] = u
                            for other in set(group.cells) - set(comb):
                                other.impossible |= other.possible & u
                                other.possible -= u
                            new_preset = True

    def bare_tex_output(self):
        self._tex_output(self.filename + "_bare.tex")
    
    def forced_tex_output(self):
        self._force_digits()
        self._tex_output(self.filename + "_forced.tex")
        
    def marked_tex_output(self):
        self._force_digits()
        self._mark_cells()
        self._tex_output(self.filename + "_marked.tex")
        
    def worked_tex_output(self):
        self._force_digits()
        self._mark_cells()
        self._solve()
        self._tex_output(self.filename + "_worked.tex")
    
    def _tex_output(self, filename):
        with open(filename, "w") as output:
            print("\\documentclass[10pt]{article}\n\\usepackage[left=0pt,right=0pt]{geometry}\n\\usepackage{tikz}\n\\usetikzlibrary{positioning}\n\\usepackage{cancel}\n\pagestyle{empty}\n\n\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n                               label=above right:{\\tiny #2},\n                               label=below left:{\\tiny #3},\n                               label=below right:{\\tiny #4}]{#5};}}\n\n\\begin{document}\n\n\\tikzset{every node/.style={minimum size=.5cm}}\n\n\\begin{center}\n\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\\hline\\hline", file = output)
            row_index = 1
            for row in self.rows:
                print(f"% Line {row_index}", file = output)
                for cell_index in range(len(row.cells)):
                    value = row.cells[cell_index].value if row.cells[cell_index].value else ""
                    a = " ".join(str(i) if i in row.cells[cell_index].possible else "\\cancel{" + str(i) + "}" if i in row.cells[cell_index].impossible else "" for i in range(1,3) if i in row.cells[cell_index].possible | row.cells[cell_index].impossible)
                    b = " ".join(str(i) if i in row.cells[cell_index].possible else "\\cancel{" + str(i) + "}" if i in row.cells[cell_index].impossible else "" for i in range(3,5) if i in row.cells[cell_index].possible | row.cells[cell_index].impossible)
                    c = " ".join(str(i) if i in row.cells[cell_index].possible else "\\cancel{" + str(i) + "}" if i in row.cells[cell_index].impossible else "" for i in range(5,7) if i in row.cells[cell_index].possible | row.cells[cell_index].impossible)
                    d = " ".join(str(i) if i in row.cells[cell_index].possible else "\\cancel{" + str(i) + "}" if i in row.cells[cell_index].impossible else "" for i in range(7,10) if i in row.cells[cell_index].possible | row.cells[cell_index].impossible)
                    e = "\\\\" if cell_index == 8 else "&" 
                    f = "\n" if cell_index in {2, 5} else " "   
                    print(f"\\N{{{a}}}{{{b}}}{{{c}}}{{{d}}}{{{value}}} " + e + f, end = "", file = output)
                g = "\\hline" if row_index % 3 else "\\hline\\hline"
                h = "" if row_index == 9 else "\n"
                print(g + h, file = output)
                row_index += 1
            print("\\end{tabular}\n\\end{center}\n\n\\end{document}", file = output)

class Group:
    def __init__(self, values):
        if len(values) != 9:
            raise SudokuError("Incorrect input")
        cells = []
        for value in values:
            if isinstance(value, Cell):
                cells.append(value)
            else:
                cells.append(Cell(value))
        self.cells = tuple(cells)
        self.presets = {}

class Cell:
    def __init__(self, value, position = (0,0,0)):
        self.value = value
        self.groups = {"row": position[0], "col": position[1], "box": position[2]}
        self.possible = set()
        self.impossible = set()
    
    def _update(self, value):
        self.value = value
        self.impossible = self.impossible | self.possible 
        self.possible = set()
        for neighbour in self.neighbours:
            if value in neighbour.possible:
                neighbour.possible -= {value}
                neighbour.impossible |= {value}

class SudokuError(Exception):
    def __init__(self, message):
        self.message = message