# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill and using the
# Alexa Skills Kid SDK (v2)
# Please visit https://alexa.design/cookbook for additional examples on
# implementing slots, dialog management,
# session persistence, api calls, and more.

import requests
import logging
import calendar
from datetime import datetime
from pytz import timezone

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler
)
from ask_sdk_core.utils import is_request_type, is_intent_name

sb = StandardSkillBuilder(table_name="cake-walk-example", auto_create_table=True)

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)


class LaunchRequestIntentHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech = "Hello! Welcome to Cake walk. What is your birthday?"
        reprompt = "I was born Nov. 6th, 2015. When were you born?"

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class HasBirthdayLaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for launch after they have set their birthday
    """
    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("year" in attr and "month" in attr and "day" in attr)

        return attributes_are_present and is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes

        year = int(attr['year'])
        month = attr['month'] # month is a string, and we need to convert it to a month index later
        day = int(attr['day'])

        # get device id / timezones
        sys_object = handler_input.request_envelope.context.system
        
        # get systems api information 
        api_endpoint = sys_object.api_endpoint
        device_id = sys_object.device.device_id
        api_access_token = sys_object.api_access_token

        # construct systems api timezone url 
        url = '{api_endpoint}/v2/devices/{device_id}/settings/System.timeZone'.format(api_endpoint=api_endpoint, device_id=device_id)
        headers = {'Authorization': 'Bearer ' + api_access_token}

        userTimeZone = ""
        try:
            r = requests.get(url, headers=headers)
            res = r.json()
            logger.info("Device API result: {}".format(str(res)))
            userTimeZone = res
        except Exception:
            handler_input.response_builder.speak("There was a problem connecting to the service")
            return handler_input.response_builder.response

        # getting the current date with the time
        now_time = datetime.now(timezone(userTimeZone))
        
        # Removing the time from the date because it affects our difference calculation
        now_date = datetime(now_time.year, now_time.month, now_time.day)
        current_year = now_time.year

        # getting the next birthday
        month_as_index = list(calendar.month_abbr).index(month[:3])
        next_birthday = datetime(current_year, month_as_index, day)

        # check if we need to adjust bday by one year
        if now_date > next_birthday:    
            next_birthday = datetime(
                year + 1,
                month_as_index,
                day
            )
            current_year += 1
        # setting the default speak_output to Happy xth Birthday!!
        # alexa will automatically correct the oridinal for you.
        # no need to worry about when to use st, th, rd
        speak_output = "Happy {}th birthday!".format(str(current_year - year))
        if now_date != next_birthday:
            diff_days = abs((now_date - next_birthday).days)
            speak_output = "Welcome back. It looks like there are \
                            {days} days until your {birthday_num}th\
                            birthday".format(
                                days=diff_days, 
                                birthday_num=(current_year-year)
                            )

        handler_input.response_builder.speak(speak_output)
        return handler_input.response_builder.response


class BirthdayIntentHandler(AbstractRequestHandler):
    """
    Handler for Capturing the Birthday
    """
    def can_handle(self, handler_input):
        return is_intent_name("CaptureBirthdayIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots

        # extract slot values
        year = slots["year"].value
        month = slots["month"].value
        day = slots["day"].value

        # save slots into session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['year'] = year
        session_attr['month'] = month
        session_attr['day'] = day

        # save session attributes as persistent attributes
        handler_input.attributes_manager.persistent_attributes = session_attr
        handler_input.attributes_manager.save_persistent_attributes()

        speech = 'Thanks, I will remember that you were born {month} {day} {year} \
            '.format(month=month, day=day, year=year)
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """
    Handler for AMAZON.HelpIntent
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can say hello to me! How can I help?"

        handler_input.response_builder.speak(
            speak_output
            ).ask(speak_output)
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """
    Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):

        speak_output = "Sorry, I couldn't understand what you said. Please try again."
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    """
    Handler for AMAZON.CancelIntent and AMAZON.StopIntent
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) \
            and is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Goodbye!"
        handler_input.response_builder.speak(speak_output)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """
    Handler for SessionEndedRequest
    """
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here
        return handler_input.response_builder.response



# register request / intent handlers
sb.add_request_handler(HasBirthdayLaunchRequestHandler())
sb.add_request_handler(LaunchRequestIntentHandler())
sb.add_request_handler(BirthdayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()