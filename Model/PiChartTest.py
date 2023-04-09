import matplotlib.pyplot as plt
import json

# Assume that you have a dictionary called 'my_dict'


my_dict = json.loads("{\"size\": [\"64GB\", 384, \"128GB\", 0, \"256GB\", 0, \"512GB\", 0], \"service_provider\": [\"Unlocked\", 384, \"AT&T\", 0, \"All Carriers\", 0, \"GSM Carriers\", 0, \"Sprint\", 0, \"T-Mobile\", 0, \"Verizon\", 0], \"product_grade\": [\"Renewed\", 384, \"Renewed Premium\", 0], \"color\": [\"Red\", 384, \"Black\", 0, \"Blue\", 0, \"Coral\", 0, \"Gold\", 0, \"Green\", 0, \"Midnight Green\", 0, \"Purple\", 0, \"Silver\", 0, \"Space Gray\", 0, \"White\", 0, \"Yellow\", 0]}")

print(my_dict)
# Extract the labels and values from the dictionary
labels = my_dict.keys()
values = my_dict.values()


for i in my_dict:
    #plt.pie(values, labels=i.keys(), autopct='%1.1f%%')
    print("hello " + i)
    for j in my_dict[i]:
        print(j)
# Set the title of the chart
plt.title('Fruit distribution')

# Show the chart
plt.show()