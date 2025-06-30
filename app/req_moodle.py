import requests,os
from dotenv import load_dotenv

load_dotenv()
from app.logger import log_info, log_error
# logging.basicConfig(level=logging.INFO, filename=os.getenv('LOG_FILE_NAME'),filemode="w")


async def find_user(crit,val): 
    log_info('Starting a user search on Moodle',criteria=crit, value=val)
    token =  os.getenv('MOODLE_TOKEN')
    function = 'core_user_get_users' 
    url = os.getenv('MOODLE_URL')

    params = {
        'wstoken': token,
        'moodlewsrestformat': 'json',
        'wsfunction': function,
        'criteria[0][key]]': crit,
        'criteria[0][value]': val
    }

    response = requests.post(url, data=params)

    if response.status_code == 200:
        log_info('The user search request on Moodle was successfully completed', 
                 response_status_code=response.status_code,response_returned_text=response.text)
            # f"Try to find ({crit} = {val}) at moodle , returned: {response.text}")
        return response.json()
    else:
        log_error('An error occurred while searching for a user on Moodle', 
                  response_status_code=response.status_code,response_returned_text=response.text)
            # f"Error when find user at moodle: {response.status_code}, {response.text}")
    

async def reg_user(user_data):
    log_info('Starting a user registration request on Moodle',user_email=user_data['emaili'])
    token =  os.getenv('MOODLE_TOKEN')
    function = 'core_user_create_users' 
    url = os.getenv('MOODLE_URL')

    params = {
        'wstoken': token,
        'moodlewsrestformat': 'json',
        'wsfunction': function,
        'users[0][username]': user_data['username'],
        'users[0][password]': user_data['password'],
        'users[0][firstname]': user_data['firstname'],
        'users[0][lastname]': user_data['lastname'],
        'users[0][email]': user_data['emaili']
    }

    # Выполнение запроса
    response = requests.post(url, data=params)

    # Проверка статуса ответа
    if response.status_code == 200:
        log_info('The user registration request on Moodle was successfully completed', 
                 response_status_code=response.status_code,response_returned_text=response.text)
        # logging.info(f"Try to reg {user_data['username']}({user_data['emaili']}) at moodle, returned: {response.json()}")
        try:
            if response["exception"]!=None:
                return "inv"
        except:
            return "reg"
    else:
        log_error('An error occurred when requesting to register a user on Moodle', 
                  response_status_code=response.status_code,response_returned_text=response.text)
        # logging.error(f"Error when reg user at moodle: {response.status_code}, {response.text}")
        return "err"

    
async def add_user_to_course(course, u_id):
    log_info('Starting a user enrollment request for a Moodle course',course_id=course)
    
    token =  os.getenv('MOODLE_TOKEN')
    function = 'enrol_manual_enrol_users' 
    url = os.getenv('MOODLE_URL')

    params = {
        'wstoken': token,
        'moodlewsrestformat': 'json',
        'wsfunction': function,
        'enrolments[0][roleid]': 5, # 5 - student
        'enrolments[0][userid]': u_id,
        'enrolments[0][courseid]': course
    }
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        log_info('The users request to enroll in a Moodle course has been successfully completed', 
                 response_status_code=response.status_code,response_returned_text=response.text)
        # logging.info(f"Added user at course {course}, returned: {response.json()}")
        return True
    else:
        log_error('An error occurred when requesting to add a user to a course on Moodle', 
                  response_status_code=response.status_code,response_returned_text=response.text)
        # logging.error(f"Error when add user at course: {response.status_code}, {response.text}")
        return False


async def add_user_to_group(group, u_id):
    log_info('Starting a request to add a user to a group on Moodle',group_id=group)
    token =  os.getenv('MOODLE_TOKEN')
    function = 'core_group_add_group_members' 
    url = os.getenv('MOODLE_URL')

    params = {
        'wstoken': token,
        'moodlewsrestformat': 'json',
        'wsfunction': function,
        'members[0][groupid]':  group,
        'members[0][userid]': u_id
    }
    response = requests.post(url, data=params)

    # Проверка статуса ответа
    if response.status_code == 200:
        log_info('The request to add a user to a group on Moodle has been successfully completed', 
                 response_status_code=response.status_code,response_returned_text=response.text)
        # logging.info(f"Try to add user to group {group}, returned: {response.json()}")
        return True
    else:
        log_error('An error occurred when requesting to add a user to a group on Moodle', 
                  response_status_code=response.status_code,response_returned_text=response.text)
        # logging.error(f"Error when add user to group: {response.status_code}, {response.text}")
        return False