from backjobs import add, test, engagment1

result_add = add.delay(4, 6)
print("Add result:", result_add.get(timeout=10))

result_test = test.delay('Hello, World!')
print("Test result:", result_test.get(timeout=10))

result_engagment1 = engagment1.delay("Test message", "Test data")
print("Engagement result:", result_engagment1.get(timeout=10))
