import  requests
import boto3


#headers are your authorization credentials for calling cult 

cookies = {
    "st": "",
    "at": ""
}

headers = {"apiKey":"",
           "Cookie": "; ".join([f"{k}={v}" for k,v in cookies.items()])
           }


#fetch classes data for the particular center 

def json_data_of_classes_for_a_center(preferred_center: object) -> object:
    classes_url = f"https://www.cult.fit/api/cult/classes?center={preferred_center}"
    json_data_of_classes = requests.get(url=classes_url, headers=headers)
    json_data_of_classes = json_data_of_classes.json()
    print(type,json_data_of_classes)
    print(json_data_of_classes)
    return json_data_of_classes
    


    

# chooses the date to book as the last availble day 

def getting_booking_date(json_data_for_center):
    booking_date = json_data_for_center['classByDateList'][-1]
    return booking_date

#checks whether there are classes available for a particular time and returns a class id if available

def checking_availability_at_preferred_time_for_center(booking_date,preffered_time):
    for class_information_by_time in booking_date['classByTimeList']:
        class_info = class_information_by_time['classes']
        for workout_info in class_info:
            if workout_info['startTime'] == preffered_time and workout_info['availableSeats'] > 0 and workout_info['workoutId'] == 69:
                class_id = workout_info['id']
                return class_id
            else:
                pass

#fetches the class id of the first available class based on preference list

def getting_class_id_of_preferred_center(list_of_preferred_time, list_of_preferred_centers):
    for time in list_of_preferred_time:
        for center in list_of_preferred_centers:
            json_data = json_data_of_classes_for_a_center(center)
            booking_date = getting_booking_date(json_data)
            class_id = checking_availability_at_preferred_time_for_center(booking_date, time)
            if class_id is not None:
                print(center)
                return class_id
        else:
            continue  
    return None  






# does the booking with booked  message if successful and with fail message and the response code if booking unsuccessfull


def booking(class_id_of_available_class):
    booking_url = f"https://www.cult.fit/api/cult/class/{class_id_of_available_class}/book"
    response = requests.post(url=booking_url,headers=headers)
    print(response.json())
    if response.status_code == 200:
        print('Class Booked. Check your cult.fit application for booking details.')
    else:
        print('Booking Failed')
        print(response.status_code)



def lambda_handler(event,context):
    preferred_centers_list = [20,130,212] #your preferred centres in order of preference
    preferred_timings_list = ['07:30:00','08:00:00','07:00:00'] #your preferred timings in order of preference

    class_id = getting_class_id_of_preferred_center(preferred_timings_list,preferred_centers_list)
    print(class_id)
    booking(class_id)