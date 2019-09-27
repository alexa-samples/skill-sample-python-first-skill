# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill and using the
# Alexa Skills Kid SDK (v2)
# Please visit https://alexa.design/cookbook for additional examples on
# implementing slots, dialog management,
# session persistence, api calls, and more.

import logging

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler
)
from ask_sdk_core.utils import is_request_type, is_intent_name

sb = StandardSkillBuilder()

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
sb.add_request_handler(LaunchRequestIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CaptureBirthdayIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
