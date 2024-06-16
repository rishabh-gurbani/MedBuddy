tools_template = {
        "type": "function",
        "function" : {
            "name" : "",
            "description" : "",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "property1" : {
                        "type": "string",
                        "description": ""
                    }
                },
                "required" : ["property1"]
            }
        }
    }

tools = [
    
    {
        "type": "function",
        "function" : {
            "name" : "findDoctors",
            "description" : 
                """
                Get the list of doctors based on the location, speciality and name. Does not allow to book appointments.
                Atleast one of the arguments is required. If no arguments are passed, all the doctors are returned.
                Ask for the location, speciality and name of doctors strictly one at a time, one by one in order of context, not all at once. 
                Can infer these arguments from chat context. If context is not clear, ask for clarification.
                STRICTLY ask for clarification if context is ambiguous.
                """,
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "location" : {
                        "type": "string",
                        "description": "Location where the doctors need to be searched"
                    },
                    "speciality" : {
                        "type": "string",
                        "description": "Speciality of the doctors"
                    },
                    "name" : {
                        "type": "string",
                        "description": "Name of the doctor if looking for a specific doctor"
                    }
                },
                "required" : ["name", "location", "speciality"]
            }
        }
    },
    {
        "type": "function",
        "function" : {
            "name" : "getDoctorSchedule",
            "description" : 
                """
                Use this function to get the schedule of the doctor based on the doctorId, day and time. Does not allow to book appointments.
                doctorId must be passed. Ask for the day and time strictly one at a time, one by one in order of context, not all at once. 
                Can infer these arguments from chat context. If context is not clear, ask for clarification.
                STRICTLY ask for clarification if context is ambiguous. 
                NEVER leak doctorId. Instead confirm the required doctor through other attributes like name, location, speciality.
                """,
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "doc_id" : {
                        "type": "string",
                        "description": "id of the doctor"
                    },
                    "day" : {
                        "type": "string",
                        "description": "Day of the week. (Eg: Monday)"
                    },  
                    "time" : {
                        "type": "string",
                        "description": "Time of the day in military format rounded to nearest half hour. (Eg: 1030, 1100)"
                    }
                },
                "required" : ["doc_id"]
            }
        }
    },
    {
        "type": "function",
        "function" : {
            "name" : "getUserAppointments",
            "description" : "Get the list of appointments of the user based on the user_id",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "user_id" : {
                        "type": "string",
                        "description": "id of the user"
                    }
                },
                "required" : ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function" : {
            "name" : "bookAppointment",
            "description" : 
                """
                This function is used to book an appointment with the doctor based on the doc_id, user_id, day and time.
                Infer the user_id, doc_id, day and time from the context of conversation. NEVER leak user_id and doc_id.
                """,
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "user_id" : {
                        "type": "string",
                        "description": "id of the user"
                    },
                    "doc_id" : {
                        "type": "string",
                        "description": "id of the doctor"
                    },
                    "day" : {
                        "type": "string",
                        "description": "Day of the week. (Eg: Monday)"
                    },
                    "time" : {
                        "type": "string",
                        "description": "Time of the day in military format rounded to nearest half hour. (Eg: 1030, 1100)"
                    }
                },
                "required" : ["doc_Id"]
            }
        }
    }
]