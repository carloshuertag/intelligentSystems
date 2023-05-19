# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from IMDBScrapper import getMovieInfo

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to movie ratings and reviews. Ask for any movie that you'd like to know about."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class MovieInformationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MovieInformation")(handler_input)
    
    def build_output(self, result, movie_title, info_key):
        if isinstance(result, list):
            speak_output = movie_title + ' was directed by: '
            directors = []
            for item in result:
                directors.append(item)
            num_directors = len(directors)
            if num_directors == 1:
                speak_output = speak_output + directors[0] + '.'
            elif num_directors == 2:
                speak_output = speak_output + directors[0] + ' and ' + directors[1] + '.'
            else:
                for i in range(num_directors - 1):
                    speak_output = speak_output + directors[i] + ', '
                speak_output = speak_output + 'and ' + directors[-1] + '.'
            return speak_output
        else:
            speak_output = 'The ' + info_key + ' of ' + movie_title
            if info_key == 'votes':
                speak_output = speak_output + ' are: '
            else:
                speak_output = speak_output + ' is: '
            speak_output = speak_output + result + '.'
        return speak_output
        
    def handle(self, handler_input):
        logger.info("In MovieInformation Intent")
        movie_title = ask_utils.get_slot_value(handler_input=handler_input, slot_name="movieName")
        info_key = ask_utils.get_slot_value(handler_input=handler_input, slot_name="movieInfo")
        movie = getMovieInfo(movie_title)
        result = movie[info_key]
        speak_output = self.build_output(result, movie_title, info_key)
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )

class MovieIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("Movie")(handler_input)
    
    def build_output(self, movie_title, movie):
        speak_output = 'Here is some information about ' + movie_title + ': '
        for key, value in movie.items():
            if isinstance(value, list):
                speak_output = speak_output + ', it was directed by: '
                directors = []
                for item in value:
                    directors.append(item)
                num_directors = len(directors)
                if num_directors == 1:
                    speak_output = speak_output + directors[0]
                elif num_directors == 2:
                    speak_output = speak_output + directors[0] + ' and ' + directors[1]
                else:
                    for i in range(num_directors - 1):
                        speak_output = speak_output + directors[i] + ', '
                    speak_output = speak_output + 'and ' + directors[-1]
            else:
                speak_output = speak_output + ', its ' + key
                if key == 'votes':
                    speak_output = speak_output + ' are: '
                else:
                    speak_output = speak_output + ' is: '
                speak_output = speak_output + value
        return speak_output
        
    def handle(self, handler_input):
        logger.info("In MovieInformation Intent")
        movie_title = ask_utils.get_slot_value(handler_input=handler_input, slot_name="movieName")
        movie = getMovieInfo(movie_title)
        speak_output = self.build_output(movie_title, movie)
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(MovieInformationIntentHandler())
sb.add_request_handler(MovieIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
