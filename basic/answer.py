import csv
import os


def main():
    user_name = input("""こんにちは！私はRobokoです。あなたの名前はなんですか？
          """)

    if os.path.exists('test.csv') is False:
        createCsv()
    else:
        rank = 1
        while True:
            restrant = recommendRestrant(rank)
            if restrant is not None:
                user_ansewr = input("""私のオススメのレストランは、{restrant}です。
                      このレストランは好きですか？[Yes/No]
                      """.format(restrant=restrant['Name']))
                if user_ansewr.lower() == "yes":
                    # update
                    res = updateCount(restrant['Name'])
                    updateCsv(res)
                    break
                else:
                    rank += 1
                    continue
            else:
                break

    lastQuestion(user_name)

              
def lastQuestion(user_name):
    favarite_restrant = input("""{name}さん。どこのレストランが好きですか？
                                """.format(name=user_name))
    
    if checkRestrant(favarite_restrant) is True:
        res = updateCount(favarite_restrant)
        updateCsv(res)
    else:
        addRetaurant(favarite_restrant)

    print("""{}さん。ありがとうございました。
            良い一日を！さようなら。
            """.format(user_name))     


def checkRestrant(restaurant_name) -> bool:
    with open('test.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Name"] == restaurant_name:
                return True
        return False
    
    
# update data
def updateCount(restaurant_name) -> dict:
    data = {}
    with open('test.csv', 'r') as csv_file:
        # fieldnames = ["Name", "Count"]
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Name"] == restaurant_name:
                new_count = int(row["Count"]) + 1
                data[row["Name"]] = new_count
            else:
                data[row["Name"]] = row["Count"]
        return data


# save csv
def updateCsv(data: dict):
    with open('test.csv', 'w+') as csv_file:
        fieldnames = ["Name", "Count"]
        writer = csv.DictWriter(csv_file, fieldnames)        
        writer.writeheader()

        for name, count in data.items():
            writer.writerow({
                "Name": name,
                "Count": count
            })


# init
def createCsv():
    with open('test.csv', 'w') as csv_file:
        field_name = ["Name", "Count"]
        writer = csv.DictWriter(csv_file, field_name)
        writer.writeheader()


# create
def addRetaurant(restrant_name):
    with open('test.csv', 'a') as csv_file:
        field_name = ["Name", "Count"]
        writer = csv.DictWriter(csv_file, field_name)
        writer.writerow({"Name": restrant_name, "Count": 1})
        
           
# get
def recommendRestrant(rank: int):
    with open('test.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        ordered_restaurants = sorted(reader, key=lambda x: x['Count'], reverse=True)
        if len(ordered_restaurants) < rank:
            return None
    return ordered_restaurants[rank - 1]
            

if __name__ == "__main__":
    main()