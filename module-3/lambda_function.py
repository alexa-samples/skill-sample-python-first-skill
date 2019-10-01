# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill and using the
# Alexa Skills Kid SDK (v2)
# Please visit https://alexa.design/cookbook for additional examples on
# implementing slots, dialog management,
# session persistence, api calls, and more.

import logging

from ask_sdk_s3.adapter import S3Adapter
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler
)
from ask_sdk_core.utils import is_request_type, is_intent_name

s3_adapter = S3Adapter(bucket_name="S3-BUCKET-NAME")
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)


class LaunchRequestIntentHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Hello! This is Cake walk. What is your birthday?"
        reprompt_text = "I was born Nov. 6th, 2015. When are you born?"
        handler_input.response_builder.speak(speak_output).ask(reprompt_text)
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

        year = attr['year']
        month = attr['month'] # month is a string, and we need to convert it to a month index later
        day = attr['day']

        # TODO:: Use the settings API to get current date and then compute how many days until user's bday
        # TODO:: Say happy birthday on the user's birthday 

        speak_output = "Welcome back it looks like there are X more days until your y-th birthday."
        handler_input.response_builder.speak(speak_output)
        return handler_input.response_builder.response


class CaptureBirthdayIntentHandler(AbstractRequestHandler):
    """
    Handler for the CaptureBirthday Intent
    """
    def can_handle(self, handler_input):
        return is_intent_name("CaptureBirthdayIntent")
    
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots

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

        speak_output = 'Thanks, I will remember that you were born {month} {day} {year}.'.format(month=month, day=day, year=year)
        handler_input.response_builder.speak(speak_output)
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

# register request / intent handlers
sb.add_request_handler(HasBirthdayLaunchRequestHandler())
sb.add_request_handler(LaunchRequestIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CaptureBirthdayIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
