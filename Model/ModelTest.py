import json
import matplotlib.pyplot as plt


dict = json.loads("{\"size\": [\"64GB\", 384, \"128GB\", 384, \"256GB\", 0, \"512GB\", 0], \"service_provider\": [\"Unlocked\", 384, \"AT&T\", 0, \"All Carriers\", 0, \"GSM Carriers\", 0, \"Sprint\", 0, \"T-Mobile\", 0, \"Verizon\", 0], \"product_grade\": [\"Renewed\", 384, \"Renewed Premium\", 0], \"color\": [\"Red\", 384, \"Black\", 0, \"Blue\", 0, \"Coral\", 0, \"Gold\", 0, \"Green\", 0, \"Midnight Green\", 0, \"Purple\", 0, \"Silver\", 0, \"Space Gray\", 0, \"White\", 0, \"Yellow\", 0]}")

print(dict)

for i in dict:

    label = []
    count = []
    total = 0

    for j in range(0, len(dict[i]), 2):
        if dict[i][j + 1] > 0:
            label.append(dict[i][j])
            count.append(dict[i][j + 1])

    print(label)
    print(count)






