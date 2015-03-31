from twisted.internet import defer
from ooni.templates.process import ProcessTest, ProcessDirector

class LanternBootstrapProcessDirector(ProcessDirector):
    """
    This Process Director monitors Lantern during its
    bootstrap and fires a callback if bootstrap is
    successful or an errback if it fails to bootstrap
    before timing out.
    """
    def __init__(self, d, finished=None, timeout=None, stdin=None):
        super(LanternProcessDirector, self)._init_(self, d, finished, timeout, stdin)
        self.bootstrapped = defer.Deferred()

    def outReceived(self, data):
        self.stdout += data
        if self.shouldClose():
            self.close("condition_met")

        # output received, see if we have bootstrapped
        if not self.bootstrapped and "About to start client (http) proxy at" in self.stdout:
            if self.timeout and self.timer:
                self.timer.cancel()
            self.bootstrapped.callback(None)

    def close(self, reason=None):
        self.reason = reason
        self.transport.loseConnection()
        self.bootstrapped.errback(reason)

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

    def setUp(self):
        d = defer.Deferred()
        command = ["/home/flashlight/go/bin/lantern_linux", "--headless"]
        self.processDirector = LanternBootstrapProcessDirector(d, finished, self.timeout)
        reactor.spawnProcess(self.processDirector, command[0], command)

    def test_lantern_bootstrapped(self):
        def addResultToReport(result):
            self.report['bootstrapped'] = True

        def addFailureToReport(failure):
            self.report['bootstrapped'] = False

        self.processDirector.bootstrapped.addCallback(addResultToReport)
        self.processDirector.bootstrapped.addErrback(addFailureToReport)
