from twisted.internet import defer
from ooni.templates.process import ProcessTest

class LanternTest(ProcessTest):

    """
    This class contains a set of tests for Lantern (https://getlantern.org).

    test_lantern_bootstrap
      Starts Lantern on Linux in --headless mode and
      determine if it bootstraps successfully or not.

    test_lantern_pass_through
      Starts Lantern and make a HTTP request for a domain that is not in Lanterns white list.
      #XXX is this worth implementing?

    test_lantern_circumvent
      Starts Lantern and make a HTTP request for a domain that is in Lanterns white list.
    """

    name = "Lantern Circumvention Tool Test"
    author = "Aaron Gibson"
    version = "0.0.1"
    timeout = 20

    @defer.inlineCallbacks
    def test_lantern_bootstrap(self):
        #xxx broken path somewhere... :(
        command = ["/home/flashlight/go/bin/lantern_linux", "--headless"]

        d = yield self.run(command)
        if "About to start client (http) proxy at" in d['stdout']:
            self.report['bootstrapped'] = True
        else:
            self.report['bootstrapped'] = False

