#Excercise 1: returning person's name and age

class Person:
   def __init__(self, name, age):
       self.name = name
       self.age = age

# Get user input for name and age
name = input("Enter your name: ")
age = int(input("Enter your age: "))  # Convert age to integer

# Create a Person object using the provided input
p1 = Person(name, age)

# Print the person's attributes
print(p1.name, "is", p1.age, "years old")

-----------------------------------------------------------------------------------
#Excercise 2: Finding sum of roman numerals

class Solution:
    def romanToInt(self, s: str) -> int:
        m= {'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000 }

        ans= 0
        
        for i in range (len(s)):
            if i <len(s)-1 and m[s[i]] <m[s[i+1]]:
                ans -=m[s[i]]
            else:
                ans+= m[s[i]]

        return ans

-----------------------------------------------------------------------------------
#Excercise 3: adding lists (l1,l2) and reversing output list

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummyHead = ListNode(0)
        tail = dummyHead
        carry = 0

        while l1 is not None or l2 is not None or carry != 0:
            digit1 = l1.val if l1 is not None else 0
            digit2 = l2.val if l2 is not None else 0

            sum = digit1 + digit2 + carry
            digit = sum % 10
            carry = sum // 10

            newNode = ListNode(digit)
            tail.next = newNode
            tail = tail.next

            l1 = l1.next if l1 is not None else None
            l2 = l2.next if l2 is not None else None

        result = dummyHead.next
        dummyHead.next = None
        return result
