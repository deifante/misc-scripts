#! /usr/bin/python
# -*- coding: utf-8 -*-
import xmlrpclib
import urllib
import json
from optparse import OptionParser
import readline
import socket
import sys
import os
import pprint

import jsonrpclib

class TerminalColours(object):
    """Class for colouring simple output to a *nix terminal"""
    BROWN   = '\033[90m'
    PINK    = '\033[95m'
    RED     = '\033[91m'
    YELLOW  = '\033[93m'
    GREEN   = '\033[92m'
    CYAN    = '\033[96m'
    TEAL    = '\033[36m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[35m'
    END     = '\033[0m'

    def make_brown(self, text):
        """Return text coloured brown

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.BROWN)

    def make_pink(self, text):
        """Return text coloured pink

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.PINK)

    def make_red(self, text):
        """Return text coloured red

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.RED)

    def make_yellow(self, text):
        """Return text coloured yellow

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.YELLOW)

    def make_green(self, text):
        """Return text coloured green

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.GREEN)

    def make_cyan(self, text):
        """Return text coloured cyan

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.CYAN)

    def make_teal(self, text):
        """Return text coloured teal

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.TEAL)

    def make_blue(self, text):
        """Return text coloured blue

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.BLUE)

    def make_magenta(self, text):
        """Return text coloured magenta

        Keyword arguments:
        text -- the text to add colouring to.

        """
        return self._make_coloured_string(text, TerminalColours.MAGENTA)

    def _make_coloured_string(self, text, colour):
        """Colours text

        Keyword arguments:
        text -- the text to add colouring to.
        colour -- The colour code that describes the
                  colour to make the text

        """
        return colour + text + TerminalColours.END

class ErrorDetails(object):
    """Provides in depth reasoning behind errors. Where available a plain
    english explanation of why the error happened and possible solutions are provided.

    """

    def __init__(self, options = None, current_operation = None):
        """Make a new ErrorDetails object.

        Keyword arguments:
        options -- The command line options object that started the program.
        used to help show where things may have gone wrong.
        current_operation -- A simple string describing what was going on
        at the time the exception occurred.

        """
        self.exception_info = sys.exc_info()
        self.options = options
        self.current_operation = current_operation
        self.error_description = None

        if socket.gaierror == self.exception_info[0] or socket.error == self.exception_info[0]:
            self.error_description = self.exception_info[1][1]
        elif xmlrpclib.Fault == self.exception_info[0]:
            self.error_description = self.exception_info[1].faultString

    def find_reason(self):
        """Return a detailed explanation and possible
        solution for the trapped exception.

        """
        term_colours = TerminalColours()
        reason = None

        if self.error_description:
            if self.error_description.find('Name or service not known') > -1:
                extra_details = None
                if self.options:
                    extra_details = 'The url requested was %s' % (term_colours.make_blue(self.options.protocol + '://' + self.options.api_url + self.options.path))

                reason = self._make_reason(self.error_description,
                                           'This is usually caused by the request url being incorrect, ' +
                                           'the server straight out denying that it knows about the url used, ' +
                                           'or even the DNS not knowing about the url being used. (You may ' +
                                           'desire to inspect your /etc/hosts file.)',
                                           extra_details)

            elif self.error_description.startswith('server error. method not found.'):
                error_lines = self.error_description.splitlines()
                reason = self._make_reason(error_lines[0],
                                           'This can be caused by not accessing the API through https or ' +
                                           'can be caused by stale method definition cache on the server. ' +
                                           'The method definition cache is found @ /tmp/xmlrpc.server.cache.' +
                                           'If all else fails, restarting Apache has been known to work.',
                                           'The function you requested was %s' % (term_colours.make_blue(error_lines[-1])))

            elif self.error_description == 'Connection refused':
                extra_details = None
                if self.options:
                    extra_details = 'The url requested was %s' % term_colours.make_blue(self.options.protocol + '://' + self.options.api_url)
                reason = self._make_reason(self.error_description, 'This is usually caused by Apache on the server being down.',
                                           extra_details)

            elif self.error_description.startswith('The specified method cannot be found'):
                error_parts = self.error_description.split(':')
                reason = self._make_reason(error_parts[0].strip(),
                                           'This is caused by calling an incorrect function from the server.' +
                                           'Check to see that the json defintion files match the methods ' +
                                           'defined in the desired class.',
                                           'The method you requested was %s' % (term_colours.make_blue(error_parts[-1].strip())))

        else:
            reason = 'Unexpected failure:\n\t%s' % term_colours.make_red(str(self.exception_info))
            if(self.current_operation):
                reason += '\nWhile %s ' % term_colours.make_yellow(self.current_operation)
        return reason

    def _make_reason(self, exception_text, exception_description, extra_details = None):
        """Convenience function for colouring text in a somewhat consistent fashion.

        Keyword arguments:
        exception_text -- The bare message from the exception.
        exception_description -- A more detailed description of why this exception
                                 may have come about and possible solutions.
        extra_details -- Additional details that may display what the system is using for
        input that may pertain to the particular issue.

        """
        term_colours = TerminalColours()
        reason = term_colours.make_red('You got the following exception:\n')
        reason += '\t%s\n' % (term_colours.make_yellow(exception_text))
        reason += '\t%s\n' % exception_description
        if extra_details:
            reason += '\n\t%s\n' % extra_details
        return reason

class BlueSkyApiTest(object):
    """Informal testing of Blue Sky functionality."""
    def __init__(self, options):
        """Initialise test object.

        Keyword arguments:
        options -- a set of options provided by OptionParser

        """
        self.options = options
        self.xdebug_param = ''
        self.server = None
        self.methods_available = None
        self.method_number = 0
        if options.xdebug_request:
            self.xdebug_param = '?XDEBUG_SESSION_START'
        elif options.profile_request:
            self.xdebug_param = '?XDEBUG_PROFILE=1'
        if self.options.method_number:
            self.options.method_number = int(self.options.method_number)

        if self.options.verbose_request:
            print 'Making request to %s' % self.options.protocol + '://' + self.options.api_url + self.options.path + self.xdebug_param

        if self.options.data_transport.lower() == 'xml':
            self.server = xmlrpclib.Server(self.options.protocol + '://' + self.options.api_url + self.options.path + self.xdebug_param, verbose=self.options.verbose_request)
        elif self.options.data_transport.lower() == 'json':
            self.server = jsonrpclib.Server(self.options.protocol + '://' + self.options.api_url + self.options.path + self.xdebug_param, verbose=self.options.verbose_request)
        elif self.options.data_transport.lower() == 'soap':
            server = None

    def get_methods_available(self):
        """Get a list of methods the server knows that it has."""
        term_colours = TerminalColours()
        try:
            if self.options.data_transport.lower() == 'xml':
                self.methods_available = self.server.system.listMethods()
            elif self.options.data_transport.lower() == 'json':
                self.json_methods_available = json.loads(urllib.urlopen(self.options.protocol + '://' + self.options.api_url + self.options.path + self.xdebug_param).read())
                self.methods_available = []
                for method_name in self.json_methods_available['methods']:
                    self.methods_available.append(method_name)
        except Exception as e:
            ed = ErrorDetails(self.options, 'Querying available methods.')
            print ed.find_reason()
            exit()

        if not (self.options.method_number != None and not self.options.verbose_request):
            print term_colours.make_pink('Methods available:\n')
            i=0
            for method in self.methods_available:
                print '\t%s %s' % ((str(i) + '.').rjust(3), term_colours.make_blue(method))
                i+=1

    def login(self):
        """Login to the server with the options provided on construction."""
        term_colours = TerminalColours()
        current_operation = 'Logging in.'
        login_result = None
        login_params = {'apiKey':self.options.api_key,
                        'username': self.options.username,
                        'password': self.options.password}
        if not (self.options.method_number != None and not self.options.verbose_request):
            print 'Logging in\n\tusername: %s\n\tpassword: %s\n\t api key: %s' % \
                (term_colours.make_yellow(self.options.username), term_colours.make_yellow(self.options.password),
                 term_colours.make_yellow(self.options.api_key))

        try:
            login_result = self.server.istockphoto.auth.getNewAuthToken(login_params)
            login_result = login_result[login_result.keys()[0]]
        except Exception as e:
            login_result = None
            ed = ErrorDetails(self.options, current_operation)
            print ed.find_reason()
            exit()

        self.token = login_result['token']
        if not (self.options.method_number != None and not self.options.verbose_request):
            print term_colours.make_green('Login successful.')

    def choose_method(self):
        """Pick a method to run from the list that the server
        has said are available.

        """
        term_colours = TerminalColours()
        if(self.options.method_number == None):
            self.method_number = int(raw_input('Choose method #:'))
            print 'Chose %s' % term_colours.make_teal(self.methods_available[self.method_number])
        else:
            self.method_number = self.options.method_number

    def show_chosen_method_details(self):
        """Provide signature and any documentation on the currently
        chosen method to run.

        """

        term_colours = TerminalColours()

        try:
            if self.options.data_transport.lower() == 'xml':
                method_signature = self.server.system.methodSignature(self.methods_available[self.method_number])

            elif self.options.data_transport.lower() == 'json':
                method_parameters = self.json_methods_available['methods'][self.methods_available[self.method_number]]['parameters']
                method_returns = self.json_methods_available['methods'][self.methods_available[self.method_number]]['returns']

                method_parameters = json.dumps(method_parameters, sort_keys=True, indent=2)
                method_returns = json.dumps(method_returns, sort_keys=True, indent=2)
                method_signature = 'Parameters:\n%s\nReturns:\n%s' % (method_parameters, method_returns)

        except Exception as e:
            ed = ErrorDetails(self.options, 'Retrieving %s method signature.' % self.methods_available[self.method_number])
            print ed.find_reason()
            exit()

        print term_colours.make_pink('Method signature:') + '\n%s' % method_signature

        if self.options.data_transport.lower() == 'json':
            return

        try:
            method_help = self.server.system.methodHelp(self.methods_available[self.method_number])
        except Exception as e:
            ed = ErrorDetails(self.options, 'Retrieving %s method help.' % self.methods_available[self.method_number])
            print ed.find_reason()
            exit()

        print term_colours.make_pink('Method help:') + '\n%s' % method_help

    def run(self):
        """Run the currently chosen method."""
        result = None
        term_colours = TerminalColours()
        if self.options.quiet == False:
            print 'Calling %s' % term_colours.make_teal(self.methods_available[self.method_number])
        try:
            if 'system.listMethods' == self.methods_available[self.method_number]:
                result = getattr(self.server, self.methods_available[self.method_number])()

            elif 'system.methodHelp' == self.methods_available[self.method_number]:
                method_argument = 'istockphoto.auth.getNewAuthToken'
                if self.options.quiet == False:
                    print 'with argument %s' % method_argument
                result = getattr(self.server, self.methods_available[self.method_number])(method_argument)

            elif 'system.methodSignature' == self.methods_available[self.method_number]:
                method_argument = 'istockphoto.auth.getNewAuthToken'
                if self.options.quiet == False:
                    print 'with argument %s' % method_argument
                result = getattr(self.server, self.methods_available[self.method_number])(method_argument)
                pass

            elif 'system.multicall' == self.methods_available[self.method_number]:
                multicall = xmlrpclib.MultiCall(self.server)
                multicall.system.listMethods()
                multicall.system.methodHelp('system.multicall')
                multicall.system.methodSignature('system.multicall')
                login_params = {'apiKey'      :self.options.api_key,
                                'username' : self.options.username,
                                'password' : self.options.password}
                multicall.istockphoto.auth.getNewAuthToken(login_params)
                result = multicall()

            elif 'istockphoto.auth.getNewAuthToken' == self.methods_available[self.method_number]:
                login_params = {'apiKey'      :self.options.api_key,
                                'username' : self.options.username,
                                'password' : self.options.password}
                result = getattr(self.server, self.methods_available[self.method_number])(login_params)

            elif 'istockphoto.auth.validateToken' == self.methods_available[self.method_number]:
                login_params = {'apiKey'   :self.options.api_key,
                                'token' :self.token}
                result = getattr(self.server, self.methods_available[self.method_number])(login_params)

            elif 'istockphoto.asset.getAssetData' == self.methods_available[self.method_number]:
                asset_data_params = {'token':self.token,
                                     'limit':1}
                result = getattr(self.server, self.methods_available[self.method_number])(asset_data_params)

            elif 'istockphoto.asset.getAssetDataById' == self.methods_available[self.method_number]:
                asset_by_id_params = {'token'   :self.token,
                                      'assetId' : int(self.options.file_id)}
                result = getattr(self.server, self.methods_available[self.method_number])(asset_by_id_params)

            elif 'istockphoto.asset.getAssetStatusSummary' == self.methods_available[self.method_number]:
                asset_by_id_params = {'token'  :self.token,
                                      'client' :'getty'}
                result = getattr(self.server, self.methods_available[self.method_number])(asset_by_id_params)

            elif 'istockphoto.asset.generateNewAssetUri' == self.methods_available[self.method_number]:
                new_uri_params = {'token'   :self.token,
                                  'assetId' :11604984}
                result = getattr(self.server, self.methods_available[self.method_number])(new_uri_params)

            elif 'istockphoto.asset.setAssetStatus' == self.methods_available[self.method_number]:
                set_status_params = {'token'     :self.token,
                                     'client'    :'getty',
                                     'assetId'   :int(self.options.file_id),
                                     'partnerId' :self.options.getty_id,
                                     'status'    :'success',
                                     'version'   :42,
                                     'message'   :self.options.message}
                result = getattr(self.server, self.methods_available[self.method_number])(set_status_params)

        except Exception as e:
            result = None
            current_operation = 'Calling %s.' % (self.methods_available[self.method_number])
            ed = ErrorDetails(self.options, current_operation)
            if self.options.quiet == False:
                reason = ed.find_reason()
                term_colours = TerminalColours()
                print reason if reason else 'Error %s (%s)' % (current_operation.lower(), term_colours.make_red(str(e)))
            return None

        term_colours = TerminalColours()
        if self.options.quiet == False:
            print 'Called %s %s. Result as follows:\n%s' % (term_colours.make_teal(self.methods_available[self.method_number]),
                                                            term_colours.make_green('successfully'),  pprint.pformat(result))
        return result

def create_bluesky_option_parser():
    """
    Create option parser
    """
    parser = OptionParser()

    parser.add_option('-c', '--protocol', action='store',      dest='protocol',        help='Intended for https vs. http.',                 default='http')
    parser.add_option('-d', '--xdebug',   action='store_true', dest='xdebug_request',  help='Make requests with ?XDEBUG_SESSION_START.',    default=False)
    parser.add_option('-e', '--message',  action='store',      dest='message',         help='Specify the outgoing message.',                default='The checksum supplied is: 0')
    parser.add_option('-f', '--path',     action='store',      dest='path',            help='Path where webservices sit.',                  default='/webservices/xmlrpc/')
    parser.add_option('-g', '--getty_id', action='store',      dest='getty_id',        help='Set the Getty Id of the file transfer.',       default=33025)
    parser.add_option('-i', '--file_id',  action='store',      dest='file_id',         help='Request a specific file.',                     default=11604984)
    parser.add_option('-k', '--api_key',  action='store',      dest='api_key',         help='API Key to use for requests.',                 default='bd0032c1dd8c8c41d66a91f5')
    parser.add_option('-m', '--method',   action='store',      dest='method_number',   help="Quickly run specified method number.",         default=None)
    parser.add_option('-o', '--profile',  action='store_true', dest='profile_request', help='Make requests with ?XDEBUG_PROFILE=1.',        default=False)
    parser.add_option('-p', '--password', action='store',      dest='password',        help='Password to use for retrieving api token.',    default='test1234')
    parser.add_option('-q', '--quiet',    action='store_true', dest='quiet',           help='Minimize printing to standard out.',           default=False)
    parser.add_option('-r', '--url',      action='store',      dest='api_url',         help='API url to query.',                            default='dev-deifante-blue.istockphoto.com')
    parser.add_option('-t', '--transport',action='store',      dest='data_transport',  help="xml|json|soap",                                default='xml')
    parser.add_option('-u', '--username', action='store',      dest='username',        help='Username to use for retrieving api token.',    default='drkwng')
    parser.add_option('-v', '--verbose',  action='store_true', dest='verbose_request', help='Display server request and response details.', default=False)

    return parser

def main():
    parser = create_bluesky_option_parser()

    (options, args) = parser.parse_args()
    api_tester = BlueSkyApiTest(options)
    api_tester.login()

    api_tester.get_methods_available()
    api_tester.choose_method()

    if options.method_number == None:
        api_tester.show_chosen_method_details()
    api_tester.run()
    return

    print 'done'

if __name__ == '__main__':
    main()
