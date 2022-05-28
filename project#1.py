user_input = input("enter the number:")
a = user_input.split(",")
for i in range(0,len(a)):
    a[i] = int(a[i])

for i in a:
    if i % 2 == 0:
        msg = "{0} is even number".format(i)

    else:
        msg = f"{i} is odd number"

    print(msg)



