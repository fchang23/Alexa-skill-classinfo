import json
import pymysql.cursors


def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.f1c6c6b2-967f-4194-80b8-6a0a53988e86"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetCourseName":
        return get_course_name(intent)
    elif intent_name == "GetCourseTime":
        return get_course_time(intent)
    elif intent_name == "GetCourseInstr":
        return get_course_instr(intent)
    elif intent_name == "GetCourseSeats":
        return get_course_seats(intent)
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...


def get_course_name(intent):
    session_attributes = {}
    card_title = "Course Name"
    reprompt_text = ""
    should_end_session = False

    coursenum = intent["slots"]["Coursenum"]["value"]

    connection = pymysql.connect(host='uvaclasses.martyhumphrey.info',
                                 user='UVAClasses',
                                 password='WR6V2vxjBbqNqbts',
                                 db='uvaclasses',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
        
            sql = "SELECT `Title` FROM `CompSci1178Data` WHERE `ClassNumber`=%s"
            cursor.execute(sql,(coursenum,))
            result = cursor.fetchone()
            speech_output = "The course " + coursenum + " is " + result['Title']

    finally:
        connection.close()

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_course_time(intent):
    session_attributes = {}
    card_title = "Course Time"
    reprompt_text = ""
    should_end_session = False

    coursenum = intent["slots"]["Coursenum"]["value"]

    connection = pymysql.connect(host='uvaclasses.martyhumphrey.info',
                                 user='UVAClasses',
                                 password='WR6V2vxjBbqNqbts',
                                 db='uvaclasses',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
        
            sql = "SELECT `Days` FROM `CompSci1178Data` WHERE `ClassNumber`=%s"
            cursor.execute(sql,(coursenum,))
            result = cursor.fetchone()
            speech_output = "The course " + coursenum + " is at " + result['Days']

    finally:
        connection.close()

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_course_instr(intent):
    session_attributes = {}
    card_title = "Course Name"
    reprompt_text = ""
    should_end_session = False

    coursenum = intent["slots"]["Coursenum"]["value"]

    connection = pymysql.connect(host='uvaclasses.martyhumphrey.info',
                                 user='UVAClasses',
                                 password='WR6V2vxjBbqNqbts',
                                 db='uvaclasses',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
        
            sql = "SELECT `Instructor` FROM `CompSci1178Data` WHERE `ClassNumber`=%s"
            cursor.execute(sql,(coursenum,))
            result = cursor.fetchone()
            speech_output = "The course's instructor is " + result['Instructor']

    finally:
        connection.close()

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_course_seats(intent):
    session_attributes = {}
    card_title = "Course Name"
    reprompt_text = ""
    should_end_session = False

    coursenum = intent["slots"]["Coursenum"]["value"]

    connection = pymysql.connect(host='uvaclasses.martyhumphrey.info',
                                 user='UVAClasses',
                                 password='WR6V2vxjBbqNqbts',
                                 db='uvaclasses',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
        
            sql1 = "SELECT `EnrollmentLimit` FROM `CompSci1178Data` WHERE `ClassNumber`=%s"
            sql2 = "SELECT `Enrollment` FROM `CompSci1178Data` WHERE `ClassNumber`=%s"
            cursor.execute(sql1,(coursenum,))
            result1 = cursor.fetchone()
            cursor.execute(sql2,(coursenum,))
            result2 = cursor.fetchone()

            speech_output = "The course has " + str(int(result1['EnrollmentLimit']) - int(result2['Enrollment'])) + " seats left"

    finally:
        connection.close()

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))




def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }