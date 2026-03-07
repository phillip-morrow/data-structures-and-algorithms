from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Difficulty, Lesson, Problem, Topic


async def seed_data(session: AsyncSession):
    arrays = Topic(
        title="Arrays & Strings",
        slug="arrays-strings",
        description="Master the fundamentals of array manipulation, two pointers, sliding window, and string operations.",
        order=1,
        icon="brackets",
    )
    session.add(arrays)
    await session.flush()

    arrays_intro = Lesson(
        topic_id=arrays.id,
        title="Array Fundamentals & Two Pointers",
        slug="array-fundamentals",
        description="Learn core array operations and the two-pointer technique.",
        order=1,
        content="""# Array Fundamentals & Two Pointers

## Key Concepts
- Arrays store elements in **contiguous memory** - O(1) access by index
- **Two Pointers** is a technique where you use two indices to traverse the array, often from opposite ends
- Common patterns: converging pointers, fast/slow pointers, same-direction pointers

## When to Use Two Pointers
- Sorted arrays where you need to find pairs
- In-place array modifications
- Palindrome checks
- Removing duplicates

## Time Complexity
- Two pointer traversal: **O(n)**
- Avoids nested loops, reducing O(n^2) to O(n)

## Example: Two Sum (Sorted Array)
```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        current = nums[left] + nums[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
    return []
```
""",
    )
    session.add(arrays_intro)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=arrays_intro.id,
            title="Two Sum (Sorted)",
            slug="two-sum-sorted",
            difficulty=Difficulty.EASY,
            description="""Given a **sorted** array of integers `nums` and a `target`, return the indices of two numbers that add up to the target.

You may assume each input has **exactly one solution**, and you may not use the same element twice.

**Example:**
```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]  (because 2 + 7 = 9)
```""",
            starter_code="""def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    # Use two pointers to find the pair
    pass
""",
            solution_code="""def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    left, right = 0, len(nums) - 1
    while left < right:
        current = nums[left] + nums[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
    return []
""",
            test_code="""assert two_sum_sorted([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_sorted([1, 2, 3, 4, 5], 9) == [3, 4]
assert two_sum_sorted([-3, -1, 0, 1, 5], 4) == [1, 4]
assert two_sum_sorted([1, 3, 5, 7], 10) == [1, 3]""",
            hints="Start with pointers at both ends. If sum is too small, move left pointer right. If too large, move right pointer left.",
            order=1,
        ),
        Problem(
            lesson_id=arrays_intro.id,
            title="Reverse String In-Place",
            slug="reverse-string",
            difficulty=Difficulty.EASY,
            description="""Write a function that reverses a list of characters **in-place**.

Do not allocate extra space - modify the input list directly.

**Example:**
```
Input: ["h", "e", "l", "l", "o"]
Output: ["o", "l", "l", "e", "h"]
```""",
            starter_code="""def reverse_string(s: list[str]) -> None:
    # Modify s in-place using two pointers
    pass
""",
            solution_code="""def reverse_string(s: list[str]) -> None:
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
""",
            test_code="""s1 = ["h", "e", "l", "l", "o"]; reverse_string(s1); assert s1 == ["o", "l", "l", "e", "h"]
s2 = ["a", "b"]; reverse_string(s2); assert s2 == ["b", "a"]
s3 = ["x"]; reverse_string(s3); assert s3 == ["x"]
s4 = []; reverse_string(s4); assert s4 == []""",
            hints="Use two pointers starting at the beginning and end. Swap elements and move inward.",
            order=2,
        ),
        Problem(
            lesson_id=arrays_intro.id,
            title="Container With Most Water",
            slug="container-most-water",
            difficulty=Difficulty.MEDIUM,
            description="""Given `n` non-negative integers `height` where each represents a vertical line, find two lines that together with the x-axis form a container that holds the most water.

Return the **maximum amount of water** a container can store.

**Example:**
```
Input: height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
```
The lines at index 1 (height 8) and index 8 (height 7) form the container with the most water: min(8,7) * (8-1) = 49.""",
            starter_code="""def max_area(height: list[int]) -> int:
    # Use two pointers from the edges
    pass
""",
            solution_code="""def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        best = max(best, area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
""",
            test_code="""assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert max_area([1, 1]) == 1
assert max_area([4, 3, 2, 1, 4]) == 16
assert max_area([1, 2, 1]) == 2""",
            hints="Start with the widest container (pointers at edges). Move the pointer with the shorter line inward - you can only potentially find a taller line.",
            order=3,
        ),
    ])

    sliding = Lesson(
        topic_id=arrays.id,
        title="Sliding Window",
        slug="sliding-window",
        description="Learn to efficiently process subarrays using the sliding window technique.",
        order=2,
        content="""# Sliding Window

## Key Concepts
- Maintain a **window** (subarray) that slides across the array
- Two types: **fixed-size** window and **variable-size** window
- Avoids recomputing from scratch each time - just add/remove elements at the edges

## Fixed Window
```python
# Sum of every subarray of size k
def fixed_window(nums, k):
    window_sum = sum(nums[:k])
    results = [window_sum]
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        results.append(window_sum)
    return results
```

## Variable Window
```python
# Smallest subarray with sum >= target
def min_subarray(nums, target):
    left = 0
    current = 0
    result = float('inf')
    for right in range(len(nums)):
        current += nums[right]
        while current >= target:
            result = min(result, right - left + 1)
            current -= nums[left]
            left += 1
    return result if result != float('inf') else 0
```
""",
    )
    session.add(sliding)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=sliding.id,
            title="Maximum Sum Subarray of Size K",
            slug="max-sum-subarray-k",
            difficulty=Difficulty.EASY,
            description="""Given an array of integers `nums` and an integer `k`, find the **maximum sum** of any contiguous subarray of size `k`.

**Example:**
```
Input: nums = [2, 1, 5, 1, 3, 2], k = 3
Output: 9  (subarray [5, 1, 3])
```""",
            starter_code="""def max_sum_subarray(nums: list[int], k: int) -> int:
    # Use a fixed-size sliding window
    pass
""",
            solution_code="""def max_sum_subarray(nums: list[int], k: int) -> int:
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
""",
            test_code="""assert max_sum_subarray([2, 1, 5, 1, 3, 2], 3) == 9
assert max_sum_subarray([1, 2, 3, 4, 5], 2) == 9
assert max_sum_subarray([5], 1) == 5
assert max_sum_subarray([-1, -2, 3, 4], 2) == 7""",
            hints="Compute the sum of the first k elements, then slide the window by adding the next element and removing the leftmost.",
            order=1,
        ),
        Problem(
            lesson_id=sliding.id,
            title="Longest Substring Without Repeating Characters",
            slug="longest-substring-no-repeat",
            difficulty=Difficulty.MEDIUM,
            description="""Given a string `s`, find the length of the **longest substring** without repeating characters.

**Example:**
```
Input: s = "abcabcbb"
Output: 3  (substring "abc")
```""",
            starter_code="""def length_of_longest_substring(s: str) -> int:
    # Use a variable sliding window with a set
    pass
""",
            solution_code="""def length_of_longest_substring(s: str) -> int:
    seen = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len
""",
            test_code="""assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("bbbbb") == 1
assert length_of_longest_substring("pwwkew") == 3
assert length_of_longest_substring("") == 0
assert length_of_longest_substring("abcdef") == 6""",
            hints="Expand the window right. When you find a duplicate, shrink from the left until the duplicate is removed. Track characters in a set.",
            order=2,
        ),
    ])

    hashmaps = Topic(
        title="Hash Maps & Sets",
        slug="hash-maps-sets",
        description="Master hash-based data structures for O(1) lookups, frequency counting, and grouping.",
        order=2,
        icon="hash",
    )
    session.add(hashmaps)
    await session.flush()

    hashmap_basics = Lesson(
        topic_id=hashmaps.id,
        title="Hash Map Fundamentals",
        slug="hashmap-fundamentals",
        description="Learn when and how to use dictionaries for optimal solutions.",
        order=1,
        content="""# Hash Map Fundamentals

## Key Concepts
- Hash maps (Python `dict`) provide **O(1) average** lookup, insert, and delete
- Perfect for: frequency counting, two-sum patterns, grouping, caching
- Trade space for time - use extra memory to avoid repeated work

## Common Patterns

### 1. Frequency Counter
```python
from collections import Counter
freq = Counter("hello")  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

### 2. Two Sum (Classic)
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

### 3. Grouping / Anagram Detection
```python
from collections import defaultdict
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```
""",
    )
    session.add(hashmap_basics)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=hashmap_basics.id,
            title="Two Sum",
            slug="two-sum",
            difficulty=Difficulty.EASY,
            description="""Given an array of integers `nums` and an integer `target`, return the **indices** of the two numbers that add up to `target`.

You may assume each input has **exactly one solution**, and you may not use the same element twice.

**Example:**
```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```""",
            starter_code="""def two_sum(nums: list[int], target: int) -> list[int]:
    # Use a hash map to find complements in O(n)
    pass
""",
            solution_code="""def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
""",
            test_code="""assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]""",
            hints="For each number, check if (target - number) is already in your hash map. If yes, you found your pair!",
            order=1,
        ),
        Problem(
            lesson_id=hashmap_basics.id,
            title="Group Anagrams",
            slug="group-anagrams",
            difficulty=Difficulty.MEDIUM,
            description="""Given a list of strings `strs`, group the **anagrams** together. You can return the answer in any order.

An anagram is a word formed by rearranging the letters of another word.

**Example:**
```
Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```""",
            starter_code="""def group_anagrams(strs: list[str]) -> list[list[str]]:
    # Group strings that are anagrams of each other
    pass
""",
            solution_code="""def group_anagrams(strs: list[str]) -> list[list[str]]:
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
""",
            test_code="""result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
result_sorted = [sorted(g) for g in result]
result_sorted.sort()
assert result_sorted == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
assert group_anagrams([""]) == [[""]]
assert group_anagrams(["a"]) == [["a"]]""",
            hints="Two strings are anagrams if they have the same sorted characters. Use sorted characters as a dictionary key.",
            order=2,
        ),
    ])

    linked = Topic(
        title="Linked Lists",
        slug="linked-lists",
        description="Understand pointer manipulation, reversal, cycle detection, and merge techniques.",
        order=3,
        icon="link",
    )
    session.add(linked)
    await session.flush()

    ll_basics = Lesson(
        topic_id=linked.id,
        title="Linked List Basics & Reversal",
        slug="linked-list-basics",
        description="Learn to traverse, reverse, and manipulate linked lists.",
        order=1,
        content="""# Linked List Basics

## Key Concepts
- Each node holds a **value** and a **pointer to the next node**
- No random access - must traverse from head: O(n)
- Insertion/deletion at known position: O(1)

## ListNode Definition
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## Reversal (Iterative)
```python
def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
```

## Floyd's Cycle Detection
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```
""",
    )
    session.add(ll_basics)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=ll_basics.id,
            title="Reverse a Linked List",
            slug="reverse-linked-list",
            difficulty=Difficulty.EASY,
            description="""Reverse a singly linked list and return the new head.

A `ListNode` class is provided:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

**Example:**
```
Input:  1 -> 2 -> 3 -> 4 -> 5
Output: 5 -> 4 -> 3 -> 2 -> 1
```""",
            starter_code="""class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    # Reverse the linked list iteratively
    pass
""",
            solution_code="""class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
""",
            test_code="""def to_list(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result
def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next
assert to_list(reverse_list(from_list([1,2,3,4,5]))) == [5,4,3,2,1]
assert to_list(reverse_list(from_list([1,2]))) == [2,1]
assert to_list(reverse_list(from_list([]))) == []""",
            hints="Use three pointers: prev, current, and next. At each step, point current.next to prev, then advance all pointers.",
            order=1,
        ),
        Problem(
            lesson_id=ll_basics.id,
            title="Detect Cycle in Linked List",
            slug="linked-list-cycle",
            difficulty=Difficulty.EASY,
            description="""Given `head`, determine if the linked list has a **cycle** in it.

A cycle exists if some node can be reached again by continuously following `next`.

Return `True` if there is a cycle, `False` otherwise.

Use Floyd's cycle detection (fast & slow pointers).""",
            starter_code="""class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head: ListNode) -> bool:
    # Use fast and slow pointers
    pass
""",
            solution_code="""class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head: ListNode) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
""",
            test_code="""n1 = ListNode(1); n2 = ListNode(2); n3 = ListNode(3); n1.next = n2; n2.next = n3; n3.next = n1
assert has_cycle(n1) == True
a1 = ListNode(1); a2 = ListNode(2); a1.next = a2
assert has_cycle(a1) == False
assert has_cycle(None) == False""",
            hints="Use two pointers moving at different speeds. If there's a cycle, the fast pointer will eventually catch the slow pointer.",
            order=2,
        ),
    ])

    stacks = Topic(
        title="Stacks & Queues",
        slug="stacks-queues",
        description="Learn LIFO and FIFO data structures for parsing, BFS, and monotonic patterns.",
        order=4,
        icon="layers",
    )
    session.add(stacks)
    await session.flush()

    stack_basics = Lesson(
        topic_id=stacks.id,
        title="Stack Fundamentals",
        slug="stack-fundamentals",
        description="Master stack-based problem solving: balanced brackets, monotonic stacks.",
        order=1,
        content="""# Stack Fundamentals

## Key Concepts
- **LIFO** (Last In, First Out)
- Python list works as a stack: `append()` to push, `pop()` to pop
- Common uses: parsing, undo operations, DFS, expression evaluation

## Valid Parentheses Pattern
```python
def is_valid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in pairs:
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0
```

## Monotonic Stack
Used to find the **next greater/smaller element** efficiently.
```python
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []  # stores indices
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            result[stack.pop()] = num
        stack.append(i)
    return result
```
""",
    )
    session.add(stack_basics)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=stack_basics.id,
            title="Valid Parentheses",
            slug="valid-parentheses",
            difficulty=Difficulty.EASY,
            description="""Given a string `s` containing only `()[]{}`, determine if the input string is **valid**.

A string is valid if:
1. Open brackets are closed by the same type of brackets
2. Open brackets are closed in the correct order
3. Every close bracket has a corresponding open bracket

**Examples:**
```
"()" -> True
"()[]{}" -> True
"(]" -> False
"([)]" -> False
"{[]}" -> True
```""",
            starter_code="""def is_valid(s: str) -> bool:
    # Use a stack to match brackets
    pass
""",
            solution_code="""def is_valid(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in pairs:
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0
""",
            test_code="""assert is_valid("()") == True
assert is_valid("()[]{}") == True
assert is_valid("(]") == False
assert is_valid("([)]") == False
assert is_valid("{[]}") == True
assert is_valid("") == True
assert is_valid("(") == False""",
            hints="Push opening brackets onto a stack. When you see a closing bracket, check if the top of the stack has the matching opening bracket.",
            order=1,
        ),
        Problem(
            lesson_id=stack_basics.id,
            title="Min Stack",
            slug="min-stack",
            difficulty=Difficulty.MEDIUM,
            description="""Design a stack that supports push, pop, top, and retrieving the minimum element in **O(1) time**.

Implement the `MinStack` class:
- `push(val)` - pushes element onto stack
- `pop()` - removes top element
- `top()` - gets top element
- `get_min()` - retrieves minimum element

**Example:**
```
stack = MinStack()
stack.push(-2)
stack.push(0)
stack.push(-3)
stack.get_min()  # returns -3
stack.pop()
stack.top()      # returns 0
stack.get_min()  # returns -2
```""",
            starter_code="""class MinStack:
    def __init__(self):
        pass

    def push(self, val: int) -> None:
        pass

    def pop(self) -> None:
        pass

    def top(self) -> int:
        pass

    def get_min(self) -> int:
        pass
""",
            solution_code="""class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def get_min(self) -> int:
        return self.min_stack[-1]
""",
            test_code="""s = MinStack(); s.push(-2); s.push(0); s.push(-3)
assert s.get_min() == -3
s.pop()
assert s.top() == 0
assert s.get_min() == -2
s2 = MinStack(); s2.push(1); s2.push(1); s2.pop()
assert s2.get_min() == 1""",
            hints="Use two stacks: one for values and one to track the current minimum. Only push to min stack when the new value is <= current min.",
            order=2,
        ),
    ])

    trees = Topic(
        title="Trees & Graphs",
        slug="trees-graphs",
        description="Navigate tree traversals, BST operations, BFS/DFS, and graph algorithms.",
        order=5,
        icon="git-branch",
    )
    session.add(trees)
    await session.flush()

    tree_basics = Lesson(
        topic_id=trees.id,
        title="Binary Tree Traversals",
        slug="binary-tree-traversals",
        description="Master inorder, preorder, postorder, and level-order traversals.",
        order=1,
        content="""# Binary Tree Traversals

## TreeNode Definition
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## Traversal Orders
- **Inorder** (Left, Root, Right) - gives sorted order for BST
- **Preorder** (Root, Left, Right) - useful for copying/serializing
- **Postorder** (Left, Right, Root) - useful for deletion
- **Level-order** (BFS) - process level by level

## Recursive Inorder
```python
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)
```

## Level-Order (BFS)
```python
from collections import deque
def level_order(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```
""",
    )
    session.add(tree_basics)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=tree_basics.id,
            title="Maximum Depth of Binary Tree",
            slug="max-depth-binary-tree",
            difficulty=Difficulty.EASY,
            description="""Given the `root` of a binary tree, return its **maximum depth**.

Maximum depth is the number of nodes along the longest path from root to the farthest leaf.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

**Example:**
```
    3
   / \\
  9  20
    /  \\
   15   7

Output: 3
```""",
            starter_code="""class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: TreeNode) -> int:
    # Use recursion
    pass
""",
            solution_code="""class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: TreeNode) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
""",
            test_code="""t1 = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert max_depth(t1) == 3
assert max_depth(TreeNode(1, None, TreeNode(2))) == 2
assert max_depth(None) == 0
assert max_depth(TreeNode(1)) == 1""",
            hints="Base case: empty tree has depth 0. Recursive case: 1 + max of left and right subtree depths.",
            order=1,
        ),
        Problem(
            lesson_id=tree_basics.id,
            title="Invert Binary Tree",
            slug="invert-binary-tree",
            difficulty=Difficulty.EASY,
            description="""Given the `root` of a binary tree, **invert** the tree (mirror it) and return its root.

**Example:**
```
Input:        Output:
    4             4
   / \\           / \\
  2   7         7   2
 / \\ / \\       / \\ / \\
1  3 6  9     9  6 3  1
```""",
            starter_code="""class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invert_tree(root: TreeNode) -> TreeNode:
    # Swap left and right children recursively
    pass
""",
            solution_code="""class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invert_tree(root: TreeNode) -> TreeNode:
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root
""",
            test_code="""def tree_to_list(root):
    if not root: return []
    result, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    return result
t = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
inverted = invert_tree(t)
assert tree_to_list(inverted) == [4, 7, 2, 9, 6, 3, 1]
assert invert_tree(None) is None""",
            hints="At each node, swap left and right children, then recursively invert both subtrees.",
            order=2,
        ),
    ])

    dp = Topic(
        title="Dynamic Programming",
        slug="dynamic-programming",
        description="Break complex problems into overlapping subproblems with memoization and tabulation.",
        order=6,
        icon="zap",
    )
    session.add(dp)
    await session.flush()

    dp_basics = Lesson(
        topic_id=dp.id,
        title="DP Fundamentals",
        slug="dp-fundamentals",
        description="Learn the core DP patterns: memoization, tabulation, and identifying subproblems.",
        order=1,
        content="""# Dynamic Programming Fundamentals

## When to Use DP
1. **Optimal substructure** - optimal solution contains optimal solutions to subproblems
2. **Overlapping subproblems** - same subproblems are solved multiple times

## Two Approaches
### Top-Down (Memoization)
```python
def fib(n, memo={}):
    if n <= 1: return n
    if n not in memo:
        memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
```

### Bottom-Up (Tabulation)
```python
def fib(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

## Common DP Patterns
- **Climbing stairs** - ways to reach a target
- **Knapsack** - maximize value with constraints
- **Longest subsequence** - LIS, LCS
- **Grid paths** - unique paths, min cost
""",
    )
    session.add(dp_basics)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=dp_basics.id,
            title="Climbing Stairs",
            slug="climbing-stairs",
            difficulty=Difficulty.EASY,
            description="""You are climbing a staircase that has `n` steps. Each time you can climb **1 or 2 steps**. How many **distinct ways** can you reach the top?

**Examples:**
```
Input: n = 2
Output: 2  (1+1 or 2)

Input: n = 3
Output: 3  (1+1+1, 1+2, 2+1)
```""",
            starter_code="""def climb_stairs(n: int) -> int:
    # Use DP - this is essentially Fibonacci!
    pass
""",
            solution_code="""def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
""",
            test_code="""assert climb_stairs(2) == 2
assert climb_stairs(3) == 3
assert climb_stairs(1) == 1
assert climb_stairs(5) == 8
assert climb_stairs(10) == 89""",
            hints="The number of ways to reach step n = ways to reach step (n-1) + ways to reach step (n-2). This is the Fibonacci sequence!",
            order=1,
        ),
        Problem(
            lesson_id=dp_basics.id,
            title="Coin Change",
            slug="coin-change",
            difficulty=Difficulty.MEDIUM,
            description="""Given an array `coins` of coin denominations and an `amount`, return the **fewest number of coins** needed to make that amount. Return `-1` if it's not possible.

**Example:**
```
Input: coins = [1, 5, 10, 25], amount = 30
Output: 2  (25 + 5)

Input: coins = [2], amount = 3
Output: -1
```""",
            starter_code="""def coin_change(coins: list[int], amount: int) -> int:
    # Use bottom-up DP
    pass
""",
            solution_code="""def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
""",
            test_code="""assert coin_change([1, 5, 10, 25], 30) == 2
assert coin_change([2], 3) == -1
assert coin_change([1], 0) == 0
assert coin_change([1, 2, 5], 11) == 3
assert coin_change([186, 419, 83, 408], 6249) == 20""",
            hints="Build a DP array where dp[i] = min coins needed for amount i. For each amount, try every coin and take the minimum.",
            order=2,
        ),
    ])

    sorting = Topic(
        title="Sorting & Searching",
        slug="sorting-searching",
        description="Implement classic sorting algorithms and master binary search patterns.",
        order=7,
        icon="arrow-up-down",
    )
    session.add(sorting)
    await session.flush()

    binary_search = Lesson(
        topic_id=sorting.id,
        title="Binary Search",
        slug="binary-search",
        description="Master the binary search pattern and its many variations.",
        order=1,
        content="""# Binary Search

## Key Concepts
- Works on **sorted** arrays
- Halves the search space each step: **O(log n)**
- Many variations: find exact, find leftmost, find rightmost, search rotated

## Classic Binary Search
```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

## Find Leftmost (Lower Bound)
```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```
""",
    )
    session.add(binary_search)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=binary_search.id,
            title="Binary Search",
            slug="binary-search-basic",
            difficulty=Difficulty.EASY,
            description="""Given a sorted array `nums` and a `target`, return the index of the target if found, otherwise return `-1`.

You must write an algorithm with **O(log n)** runtime complexity.

**Example:**
```
Input: nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4
```""",
            starter_code="""def search(nums: list[int], target: int) -> int:
    # Implement binary search
    pass
""",
            solution_code="""def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
""",
            test_code="""assert search([-1, 0, 3, 5, 9, 12], 9) == 4
assert search([-1, 0, 3, 5, 9, 12], 2) == -1
assert search([5], 5) == 0
assert search([1, 2, 3, 4, 5], 1) == 0""",
            hints="Maintain lo and hi pointers. Compare middle element to target. Narrow the search space by half each iteration.",
            order=1,
        ),
        Problem(
            lesson_id=binary_search.id,
            title="Search in Rotated Sorted Array",
            slug="search-rotated-array",
            difficulty=Difficulty.MEDIUM,
            description="""A sorted array has been **rotated** at some pivot. Given `nums` and a `target`, return its index or `-1`.

You must achieve **O(log n)** time.

**Example:**
```
Input: nums = [4, 5, 6, 7, 0, 1, 2], target = 0
Output: 4
```""",
            starter_code="""def search_rotated(nums: list[int], target: int) -> int:
    # Modified binary search for rotated array
    pass
""",
            solution_code="""def search_rotated(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
""",
            test_code="""assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
assert search_rotated([1], 0) == -1
assert search_rotated([3, 1], 1) == 1""",
            hints="At each step, one half is sorted. Check if the target falls in the sorted half. If yes, search there; otherwise search the other half.",
            order=2,
        ),
    ])

    heaps = Topic(
        title="Heaps & Priority Queues",
        slug="heaps",
        description="Use heaps for top-K problems, merge K lists, and median finding.",
        order=8,
        icon="trophy",
    )
    session.add(heaps)
    await session.flush()

    heap_basics = Lesson(
        topic_id=heaps.id,
        title="Heap Fundamentals",
        slug="heap-fundamentals",
        description="Learn to use Python's heapq for efficient min/max operations.",
        order=1,
        content="""# Heap Fundamentals

## Key Concepts
- A heap is a complete binary tree where parent <= children (min-heap)
- Python `heapq` provides a **min-heap**
- Insert: O(log n), Extract min: O(log n), Peek min: O(1)

## Python heapq
```python
import heapq

# Create heap
nums = [3, 1, 4, 1, 5]
heapq.heapify(nums)         # O(n) - converts list to heap in-place

heapq.heappush(nums, 2)     # push
smallest = heapq.heappop(nums)  # pop smallest

# Top K largest
top_3 = heapq.nlargest(3, nums)

# For max-heap, negate values
max_heap = []
heapq.heappush(max_heap, -val)
max_val = -heapq.heappop(max_heap)
```
""",
    )
    session.add(heap_basics)
    await session.flush()

    session.add_all([
        Problem(
            lesson_id=heap_basics.id,
            title="Kth Largest Element",
            slug="kth-largest",
            difficulty=Difficulty.MEDIUM,
            description="""Given an integer array `nums` and an integer `k`, return the **kth largest** element in the array.

Note: it is the kth largest in **sorted order**, not the kth distinct element.

**Example:**
```
Input: nums = [3, 2, 1, 5, 6, 4], k = 2
Output: 5
```""",
            starter_code="""def find_kth_largest(nums: list[int], k: int) -> int:
    # Use a min-heap of size k
    pass
""",
            solution_code="""import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]
""",
            test_code="""assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
assert find_kth_largest([1], 1) == 1
assert find_kth_largest([7, 6, 5, 4, 3, 2, 1], 5) == 3""",
            hints="Maintain a min-heap of size k. The top of the heap will be the kth largest. Only push elements that are larger than the heap's min.",
            order=1,
        ),
    ])

    await session.commit()
