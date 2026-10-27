## Idea of the solution

We used dynamic programming on the tree. For every employee u there are three states:

| State | Meaning |
|-------|---------|
| 0 | u is in the team |
| 1 | u is not in the team, but u's manager is |
| 2 | u is not in the team and u's manager is not in the team either |

`DP[u][s]` is the smallest number of team members needed inside the subtree of u for that state. For the CEO state 1 is not possible because the CEO has no manager, so the answer is `min(DP[root][0], DP[root][2])`.

The recurrences are:

- `DP[u][0] = 1 + sum over children v of min(DP[v][0], DP[v][1])`
- `DP[u][1] = sum over children v of DP[v][2]`
- `DP[u][2] = min over children w of ( DP[w][0] + sum of DP[v][2] over the other children v )`

For a leaf, `DP = [1, 0, infinity]`.

Some `DP[v][2]` values can be infinity, so the code counts how many children have an infinite state 2 (`inf_count`). If it is more than one, `DP[u][2]` is infinity. If it is exactly one, that child has to be the one chosen in the team. Because of this the state 2 value can be found in O(number of children) time instead of recomputing the sum for every choice.

After the DP is filled in, we trace back from the root and use `best_sub_state2` (the child chosen for state 2) to get the actual team members and not just the size.

The full proof of correctness, complexity analysis and pseudocode are in the report (`DAA.pdf`).

## Complexity

- Time: O(N), where N is the number of employees
- Space: O(N)

## Files

- `python_code.py` : the implementation
- `DAA.pdf` : the report (explanation, proof, complexity, pseudocode)
- `README.md` : this file

## How to run

You only need Python 3. No extra libraries are needed.

```
python python_code.py
```

This runs the example at the bottom of the file.

## How to give the input

The program does not read from the keyboard or from a file. The tree is written inside the Python file.

The easiest way is `build_tree`. You write the tree as a dictionary where each employee is followed by the list of their direct subordinates, and then give the name of the CEO:

```python
tree = build_tree({
    "CEO":   ["Asha", "Bilal"],
    "Asha":  ["Chen", "Dev"],
    "Bilal": ["Esha", "Farid"],
}, "CEO")

print(get_comms_team(tree))
```

Employees who have no subordinates (like Chen, Dev, Esha and Farid) do not need their own line. `get_comms_team` returns a list with the names of the team members.

You can also build the tree by hand using `TreeNode` (this is what the example at the bottom of `python_code.py` does):

```python
root = TreeNode("CEO")
m1 = TreeNode("M1")
root.subordinates = [m1]
```

## Examples

### Example 1

Input (the hierarchy):

```
CEO   -> Asha, Bilal
Asha  -> Chen, Dev
Bilal -> Esha, Farid
```

(The `->` is only how we write the hierarchy here. In the program it is the dictionary shown above.)

Output:

```
Team: Asha, Bilal, CEO
Size: 3
```

Checking it:
- Chen and Dev are not in the team and their only team neighbour is Asha.
- Esha and Farid are not in the team and their only team neighbour is Bilal.
- The CEO, Asha and Bilal are in the team, so the rule does not apply to them.
- Asha and Bilal alone would not work. The CEO would then be outside the team with two team members who know the CEO's work, but the rule needs exactly one. So the CEO has to be in the team.

### Example 2

Input (the hierarchy):

```
CEO -> M1, M2
M1  -> E1, E2
M2  -> E3
```

Output:

```
Team: M1, E3
Size: 2
```

Checking it:
- The CEO is not in the team and the only team member who knows the CEO's work is M1 (M2 is not in the team).
- M2 is not in the team and its only team neighbour is E3.
- E1 and E2 are not in the team and their only team neighbour is M1.

The names can come out in any order, because the team is built from a set.

## Testing

We compared the output with a brute force solution (trying every subset of employees) on 3000 random trees with up to 13 employees. The size of the team matched every time and the team that was returned was valid every time.

## Things to keep in mind

- The code uses recursion, so for a very deep hierarchy (for example around 1000 or more levels in a single chain) Python gives a `RecursionError`. If that happens, increase the limit by adding this at the top of the file:

  ```python
  import sys
  sys.setrecursionlimit(10**6)
  ```

- The team is returned as a list of `val` (the name). So two employees should not have the same name, otherwise they will be counted as one.
- There can be more than one minimum team. The program gives one of them.
