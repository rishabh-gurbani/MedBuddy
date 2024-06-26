import db.mongo as mongo
from bson.objectid import ObjectId
from db.time_rounder import roundtime

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
times = ["1000", "1030", "1100", "1130", "1200", "1230", "1300", "1330", "1400", "1430", "1500", "1530", "1600", "1630", "1700", "1730", "1800", "1830", "1900", "1930", "2000", "2030", "2100", "2130"]

def findDoctors(location:str|None = None, speciality:str|None = None, name:str|None = None):
    """Get the list of doctors based on the location, speciality and name. If no arguments are passed, all the doctors are returned."""
    if (not isinstance(location, str) and location is not None) or (not isinstance(speciality, str) and speciality is not None) or( not isinstance(name, str) and name is not None):
        return {'status' : False, "error" : f"Invalid data types sent {type(location)} {type(speciality)} {type(name)}"}
    else:
        query = {}

        if location is not None:
            query["location"] = {"$regex": location, "$options": "i"}

        if speciality is not None:
            query["speciality"] = {"$regex": speciality, "$options": "i"}

        if name is not None:
            query["name"] = {"$regex": name, "$options": "i"}

        request = mongo.fetch_documents("MedBuddy", "docs", query)

        if not request['status']:
            return {"status" : False, "error" : f"Module -> mongo_call | Error -> Mongo | error  :  {request['error']}"}
        else:
            response = request['data']
            for doc in response:
                doc['_id'] = str(doc['_id'])
                doc.pop('booked_slots')
            return {'status' : True, 'data' : response}
        
def getDoctorSchedule(doc_id , day = None, time = None):
    """Get the schedule of the doctor based on the day and time. If no arguments are passed, the schedule of the current day and time is returned."""
    doc_id = ObjectId(doc_id)
    curr_time, curr_day = roundtime()

    if time is None and day is None: 
        time, day = curr_time, curr_day

    if time is None and day is not None:
        if day == curr_day:
            time = curr_time
        else:
            time = "1000"
    
    if time is not None and day is None:
        day = curr_day
    
    try:
        day = days.index(day)
        time = times.index(time)
    except ValueError as ve:
        print("Value Error raised in mongo_call, getDocSchedule", "day : ",day, "time : ",time)
        return {'status' : True, "data" : []}

    query = {"_id" : doc_id}
    request = mongo.fetch_documents("MedBuddy", "docs", query)
    if not request['status']:
        return {"status" : False, "error" : f"Module -> mongo_call | Error -> Mongo | error  :  {request['error']}"}
    else:
        response = request['data']
        if len(response) < 1: 
            return {'status' : False, 'data' : [], "error" : "No doc Found........"} 
        response = response[0]
        response = response['booked_slots']
        response = response[day][time:]
        return_list = []
        for _ in range(time, time + len(response)):
            if not response[_ - time]:
                return_list.append([times[_], not response[_ - time]])
        return {'status' : True, 'data' : return_list}
        
def getUserAppointments(user_id):
    """Get the appointments of the user based on the user_id."""
    user_id = ObjectId(user_id)
    if not isinstance(user_id, ObjectId):
        return {'status': False, "error": f"Invalid data type sent {type(user_id)}"}
    else:
        query = {"_id": user_id}
        request = mongo.fetch_documents("MedBuddy", "users", query)
        if not request['status']:
            return {"status": False, "error": f"Module -> mongo_call | Error -> Mongo | error  :  {request['error']}"}
        else:
            response = request['data']
            if len(response) < 1:
                return {'status': False, 'data': [], "error": "No user Found....."}
            response = response[0]
            appointments = response['appointments']
            appointments_with_names = []
            for appointment in appointments:
                doc_id = appointment['doc_id']
                doc_details = mongo.fetch_documents("MedBuddy", "docs", {"_id": ObjectId(doc_id)})
                if doc_details['status'] and len(doc_details['data']) > 0:
                    doc_name = doc_details['data'][0]['name']
                    appointment['doc_name'] = doc_name
                    appointments_with_names.append(appointment)
            return {'status': True, 'data': appointments_with_names}

def bookAppointment(doc_id, day, time, user_id):
    """Book an appointment based on the doc_id, day, time and user_id."""
    doc_id, user_id = ObjectId(doc_id), ObjectId(user_id)
    if not isinstance(doc_id, ObjectId) or not isinstance(user_id, ObjectId) or (day not in days) or (time not in times):
        return {'status' : False, "error" : f"Invalid data types sent {type(doc_id)} {type(day)} {type(time)} {type(user_id)}"}
    else:
        day, time = days.index(day), times.index(time)
        status = True
        docToReplace = mongo.fetch_documents("MedBuddy", "docs", {'_id' : doc_id})['data']
        userToReplace = mongo.fetch_documents("MedBuddy", "users", {'_id' : user_id})['data']
        if len(docToReplace) < 1 or len(userToReplace) < 1:
            return {"status" : False, "data" : "", "error" : f"Empty list returned doc{docToReplace} user {userToReplace}"}
        else:
            docToReplace = docToReplace[0]['booked_slots']
            userToReplace = userToReplace[0]['appointments']

        if docToReplace[day][time] == False:
            docToReplace[day][time] = True
        else:
            return {"status" : False, "data" : [], "error" : "ALREADY BOOKED"}
        
        status = status and mongo.update_document("MedBuddy", "docs", "_id", doc_id, "booked_slots", docToReplace)['status']
        userToReplace.append({"doc_id" : doc_id, "day" : days[day] ,"time" : times[time]})
        status = status and mongo.update_document("MedBuddy", "users", "_id", user_id, "appointments", userToReplace)['status']
        return {'status' : status, 'data': "Appointment booked", "error" : ""}

